use std::rc::Rc;
use std::io::Read;
use std::cmp::Ordering;
use crate::lex::{Lex, Token};
use crate::bytecode::ByteCode;
use crate::value::Value;
use crate::utils::ftoi;

type FnBc2u8 = fn(u8, u8) -> ByteCode;
type FnBc3u8 = fn(u8, u8, u8) -> ByteCode;
type FnBcBool = fn(u8, u8, bool) -> ByteCode;

// expression description, inner layer between source code and byte code
#[derive(Debug, PartialEq)]
enum ExpDesc {
    // constants
    Nil,
    Boolean(bool),
    Integer(i64),
    Float(f64),
    String(Vec<u8>),

    // variables
    Local(usize), // including temprary variables on stack
    Upvalue(usize),

    // table index
    Index(usize, usize),
    IndexField(usize, usize),
    IndexInt(usize, u8),
    IndexUpField(usize, usize), // covers global variables

    // function call
    Function(usize),
    Closure(usize),
    Call(usize, usize),
    VarArgs,

    // arithmetic operators
    UnaryOp(FnBc2u8, usize), // (opcode, operand)
    BinaryOp(FnBc3u8, usize, usize), // (opcode, left-operand, right-operand)

    // binaray logical operators: 'and', 'or'
    Test(Box<ExpDesc>, Vec<usize>, Vec<usize>), // (condition, true-list, false-list)

    // relational operators, e.g. '==', '<='
    Compare(FnBcBool, usize, usize, Vec<usize>, Vec<usize>),
}

// see discharge_const()
enum ConstStack {
    Const(usize),
    Stack(usize),
}

// mark both goto and label
#[derive(Debug)]
struct GotoLabel {
    name: String,
    icode: usize,
    nvar: usize,
}

// index of locals/upvalues in upper functions
#[derive(Debug)]
pub enum UpIndex {
    Local(usize),
    Upvalue(usize),
}

// core struct, generated in parse phase and executed in VM
#[derive(Debug, Default)]
pub struct FuncProto {
    pub has_varargs: bool,
    pub nparam: usize,
    pub constants: Vec<Value>,
    pub upindexes: Vec<UpIndex>,
    pub byte_codes: Vec<ByteCode>,
}

// level of inner functions, used for matching upvalue
#[derive(Debug, Default)]
struct Level {
    locals: Vec<(String, bool)>, // (name, referred-as-upvalue)
    upvalues: Vec<(String, UpIndex)>,
}

#[derive(Debug)]
struct ParseContext<R: Read> {
    levels: Vec<Level>,
    lex: Lex<R>,
}

#[derive(Debug)]
struct ParseProto<'a, R: Read> {
    // return to VM to execute
    fp: FuncProto,

    // internal stuff for parsing
    sp: usize,
    break_blocks: Vec<Vec<usize>>,
    continue_blocks: Vec<Vec<(usize, usize)>>,
    gotos: Vec<GotoLabel>,
    labels: Vec<GotoLabel>,
    ctx: &'a mut ParseContext<R>,
}

impl<'a, R: Read> ParseProto<'a, R> {
    // BNF:
    //   block ::= {stat} [retstat]
    //   stat ::= `;` |
    //     varlist `=` explist |
    //     functioncall |
    //     label |
    //     break |
    //     goto Name |
    //     do block end |
    //     while exp do block end |
    //     repeat block until exp |
    //     if exp then block {elseif exp then block} [else block] end |
    //     for Name `=` exp `,` exp [`,` exp] do block end |
    //     for namelist in explist do block end |
    //     function funcname funcbody |
    //     local function Name funcbody |
    //     local attnamelist [`=` explist]
    fn block(&mut self) -> Token {
        let nvar = self.local_num();
        let end_token = self.block_scope();
        self.local_expire(nvar);
        end_token
    }

    // same with block() but without expiring internal local variables
    fn block_scope(&mut self) -> Token {
        let igoto = self.gotos.len();
        let ilabel = self.labels.len();
        loop {
            // reset sp before each statement
            self.sp = self.local_num();

            match self.ctx.lex.next() {
                Token::SemiColon => (),
                t@Token::Name(_) | t@Token::ParL => {
                    // this is not standard!
                    if self.try_continue_stat(&t) {
                        continue;
                    }

                    // functioncall and var-assignment both begin with
                    // `prefixexp` which begins with `Name` or `(`.
                    let desc = self.prefixexp(t);
                    if let ExpDesc::Call(ifunc, narg_plus) = desc {
                        // prefixexp() matches the whole functioncall statement.
                        let code = ByteCode::Call(ifunc as u8, narg_plus as u8, 0);
                        self.fp.byte_codes.push(code);
                    } else {
                        // prefixexp() matches only the first variable, so we
                        // continue the statement
                        self.assignment(desc);
                    }
                }
                Token::Local =>
                    if self.ctx.lex.peek() == &Token::Function {
                        self.local_function()
                    } else {
                        self.local_variables()
                    }
                Token::Function => self.function_stat(),
                Token::If => self.if_stat(),
                Token::While => self.while_stat(),
                Token::Repeat => self.repeat_stat(),
                Token::For => self.for_stat(),
                Token::Break => self.break_stat(),
                Token::Do => self.do_stat(),
                Token::DoubColon => self.label_stat(igoto),
                Token::Goto => self.goto_stat(),
                Token::Return => self.ret_stat(),
                t => {
                    self.labels.truncate(ilabel);
                    break t;
                }
            }
        }
    }

    // BNF:
    //   local attnamelist [`=` explist]
    //   attnamelist ::=  Name attrib {`,` Name attrib}
    fn local_variables(&mut self) {
        // variable names
        let mut vars = vec![self.read_name()];
        while self.ctx.lex.peek() == &Token::Comma {
            self.ctx.lex.next();
            vars.push(self.read_name());
        }

        if self.ctx.lex.peek() == &Token::Assign {
            // explist
            self.ctx.lex.next();
            self.explist_want(vars.len());
        } else {
            // no exp, load nils
            let code = ByteCode::LoadNil(self.sp as u8, vars.len() as u8);
            self.fp.byte_codes.push(code);
        }

        // append vars into self.locals after evaluating explist
        for var in vars.into_iter() {
            self.local_new(var);
        }
    }

    // BNF:
    //   local function Name funcbody
    fn local_function(&mut self) {
        self.ctx.lex.next();
        let name = self.read_name();
        println!("== function: {name}");

        // create `name` local variable before parsing funcbody(),
        // so the function can be called in body as recursion.
        self.local_new(name);

        let f = self.funcbody(false);
        self.discharge(self.sp, f);
    }

    // BNF:
    //   function funcname funcbody
    //   funcname = Name {`.` Name} [`:` Name]
    fn function_stat(&mut self) {
        let name = self.read_name();
        let mut desc = self.simple_name(name);

        let with_self = loop {
            match self.ctx.lex.peek() {
                Token::Dot => { // `.` Name
                    self.ctx.lex.next();
                    let name = self.read_name();
                    let t = self.discharge_any(desc);
                    desc = ExpDesc::IndexField(t, self.add_const(name));
                }
                Token::Colon => { // `:` Name
                    self.ctx.lex.next();
                    let name = self.read_name();
                    let t = self.discharge_any(desc);
                    desc = ExpDesc::IndexField(t, self.add_const(name));

                    break true;
                }
                _ => {
                    break false;
                }
            }
        };

        let body = self.funcbody(with_self);
        self.assign_var(desc, body);
    }

    // BNF:
    //   funcbody ::= `(` [parlist] `)` block end
    //   parlist ::= namelist [`,` `...`] | `...`
    //   namelist ::= Name {`,` Name}
    fn funcbody(&mut self, with_self: bool) -> ExpDesc {
        // parameter list
        let mut has_varargs = false;
        let mut params = Vec::new();
        if with_self {
            params.push(String::from("self"));
        }
        self.ctx.lex.expect(Token::ParL);
        loop {
            match self.ctx.lex.next() {
                Token::Name(name) => {
                    params.push(name);
                    match self.ctx.lex.next() {
                        Token::Comma => (),
                        Token::ParR => break,
                        t => panic!("invalid parameter {t:?}"),
                    }
                }
                Token::Dots => {
                    has_varargs = true;
                    self.ctx.lex.expect(Token::ParR);
                    break;
                },
                Token::ParR => break,
                t => panic!("invalid parameter {t:?}"),
            }
        }

        // body
        let proto = chunk(self.ctx, has_varargs, params, Token::End);

        let no_upvalue = proto.upindexes.is_empty();
        let iconst = self.add_const(Value::LuaFunction(Rc::new(proto)));
        if no_upvalue {
            ExpDesc::Function(iconst)
        } else {
            ExpDesc::Closure(iconst)
        }
    }

    // BNF:
    //   varlist = explist
    //   varlist ::= var {`,` var}
    fn assignment(&mut self, first_var: ExpDesc) {
        // read varlist into @vars
        let mut vars = vec![first_var];
        loop {
            match self.ctx.lex.next() {
                Token::Comma => { // more variable
                    let token = self.ctx.lex.next();
                    vars.push(self.prefixexp(token));
                }
                Token::Assign => break,
                t => panic!("invalid assign {t:?}"),
            }
        }

        let sp0 = self.sp;
        let (mut nexp, last_exp) = self.explist();

        // assignment last variable
        match (nexp + 1).cmp(&vars.len()) {
            Ordering::Equal => {
                // assign last variable directly to avoid potential discharging
                let last_var = vars.pop().unwrap();
                self.assign_var(last_var, last_exp);
            }
            Ordering::Less => {
                // expand last expressions
                self.discharge_expand_want(last_exp, vars.len() - nexp);
                nexp = vars.len();
            }
            Ordering::Greater => {
                // drop extra exps
                nexp = vars.len();
            }
        }

        // assign previous variables from tmp registers, in reverse order
        while let Some(var) = vars.pop() {
            nexp -= 1;
            self.assign_from_stack(var, sp0 + nexp);
        }
    }

    // BNF:
    //   if exp then block {elseif exp then block} [else block] end
    fn if_stat(&mut self) {
        let mut jmp_ends = Vec::new();

        // == if exp then block
        let mut end_token = self.do_if_block(&mut jmp_ends);

        // == {elseif exp then block}
        while end_token == Token::Elseif {
            end_token = self.do_if_block(&mut jmp_ends);
        }

        // == [else block]
        if end_token == Token::Else {
            end_token = self.block();
        }

        assert_eq!(end_token, Token::End);

        let iend = self.fp.byte_codes.len() - 1;
        for i in jmp_ends.into_iter() {
            self.fp.byte_codes[i] = ByteCode::Jump((iend - i) as i16);
        }
    }

    fn do_if_block(&mut self, jmp_ends: &mut Vec<usize>) -> Token {
        let condition = self.exp();
        let false_list = self.test_or_jump(condition);

        self.ctx.lex.expect(Token::Then);

        let end_token = self.block();

        // If there are following 'elseif' or 'else' blocks,
        // jump to the very end of this whole if-statment at the
        // end of this block.
        // Make a fake byte-code to hold the place, and fix it
        // at the end of whole if-statment.
        if matches!(end_token, Token::Elseif | Token::Else) {
            self.fp.byte_codes.push(ByteCode::Jump(0));
            jmp_ends.push(self.fp.byte_codes.len() - 1);
        }

        self.fix_test_list(false_list);

        end_token
    }

    // BNF:
    //   while exp do block end
    fn while_stat(&mut self) {
        let istart = self.fp.byte_codes.len();

        let condition = self.exp();
        let false_list = self.test_or_jump(condition);

        self.ctx.lex.expect(Token::Do);

        self.push_loop_block();

        assert_eq!(self.block(), Token::End);

        // jump back
        let iend = self.fp.byte_codes.len();
        self.fp.byte_codes.push(ByteCode::Jump(-((iend - istart) as i16) - 1));

        self.pop_loop_block(istart);

        self.fix_test_list(false_list);
    }

    // BNF:
    //   repeat block until exp
    fn repeat_stat(&mut self) {
        let istart = self.fp.byte_codes.len();

        self.push_loop_block();

        let nvar = self.local_num();

        assert_eq!(self.block_scope(), Token::Until);
        let iend = self.fp.byte_codes.len();

        let condition = self.exp();
        let false_list = self.test_or_jump(condition);
        self.fix_test_list_to(false_list, istart);

        self.pop_loop_block(iend);

        // expire internal local variables AFTER reading condition exp
        // and pop_loop_block()
        self.local_expire(nvar);
    }

    // * numerical: for Name `=` ...
    // * generic:   for Name {, Name} in ...
    fn for_stat(&mut self) {
        let name = self.read_name();
        if self.ctx.lex.peek() == &Token::Assign {
            self.numerical_for(name);
        } else {
            self.generic_for(name);
        }
    }

    // BNF:
    //   for Name `=` exp `,` exp [`,` exp] do block end
    fn numerical_for(&mut self, name: String) {
        self.ctx.lex.next(); // skip `=`

        // 2 or 3 exps
        let (nexp, last_exp) = self.explist();
        self.discharge(self.sp, last_exp);

        match nexp + 1 {
            2 => self.discharge(self.sp, ExpDesc::Integer(1)),
            3 => (),
            _ => panic!("invalid numerical for exp"),
        }

        // create 3 local variables: the first is iterator,
        // and the other two to keep stack positions.
        self.local_new(name);
        self.local_new(String::from(""));
        self.local_new(String::from(""));

        self.ctx.lex.expect(Token::Do);

        // ByteCode::ForPrepare, without argument
        self.fp.byte_codes.push(ByteCode::ForPrepare(0, 0));
        let iprepare = self.fp.byte_codes.len() - 1;
        let iname = self.sp - 3;

        self.push_loop_block();

        // parse block!
        assert_eq!(self.block(), Token::End);

        // expire 3 local variables above, before ByteCode::ForLoop
        self.local_expire(self.local_num() - 3);

        // ByteCode::ForLoop, and fix ByteCode::ForPrepare above
        let d = self.fp.byte_codes.len() - iprepare;
        self.fp.byte_codes.push(ByteCode::ForLoop(iname as u8, d as u16));
        self.fp.byte_codes[iprepare] = ByteCode::ForPrepare(iname as u8, d as u16);

        self.pop_loop_block(self.fp.byte_codes.len() - 1);
    }

    // BNF:
    //   stat ::= for namelist in explist do block end
    //   namelist ::= Name {`,` Name}
    fn generic_for(&mut self, name: String) {
        // namelist
        let mut vars = vec![name];
        loop {
            match self.ctx.lex.next() {
                Token::Comma => continue,
                Token::In => break,
                Token::Name(name) => vars.push(name),
                _ => panic!("invalid generic_for namelist"),
            }
        }

        // explist
        let iter = self.sp;
        self.explist_want(3);

        let nvar = vars.len();
        self.local_new(String::from("")); // iterator function
        self.local_new(String::from("")); // immutable state
        self.local_new(String::from("")); // control variable
        for var in vars.into_iter() {
            self.local_new(var);
        }

        self.ctx.lex.expect(Token::Do);

        // jump to ByteCode::ForCallLoop at end of block
        self.fp.byte_codes.push(ByteCode::Jump(0));
        let ijump = self.fp.byte_codes.len() - 1;

        self.push_loop_block();

        // parse block!
        assert_eq!(self.block(), Token::End);

        // expire local variables above, before ByteCode::Jump
        self.local_expire(self.local_num() - 3 - nvar);

        // ByteCode::ForCallLoop
        // call the iter function and check the control variable
        let d = self.fp.byte_codes.len() - ijump;
        self.fp.byte_codes[ijump] = ByteCode::Jump(d as i16 - 1);
        if let Ok(d) = u8::try_from(d) {
            self.fp.byte_codes.push(ByteCode::ForCallLoop(iter as u8, nvar as u8, d as u8));
        } else {
            self.fp.byte_codes.push(ByteCode::ForCallLoop(iter as u8, nvar as u8, 0));
            self.fp.byte_codes.push(ByteCode::Jump(-(d as i16) - 1));
        }

        self.pop_loop_block(self.fp.byte_codes.len() - 1);
    }

    fn break_stat(&mut self) {
        let Some(breaks) = self.break_blocks.last_mut() else {
            panic!("break outside loop");
        };
        self.fp.byte_codes.push(ByteCode::Jump(0));
        breaks.push(self.fp.byte_codes.len() - 1);
    }

    fn try_continue_stat(&mut self, name: &Token) -> bool {
        let Token::Name(name) = name else { return false; };
        if name.as_str() != "continue" {
            return false;
        }
        if !matches!(self.ctx.lex.peek(), Token::End | Token::Elseif | Token::Else) {
            return false;
        }

        let nvar = self.local_num();
        let Some(continues) = self.continue_blocks.last_mut() else {
            panic!("continue outside loop");
        };
        self.fp.byte_codes.push(ByteCode::Jump(0));
        continues.push((self.fp.byte_codes.len() - 1, nvar));
        true
    }

    // before entering loop block
    fn push_loop_block(&mut self) {
        self.break_blocks.push(Vec::new());
        self.continue_blocks.push(Vec::new());
    }
    // after leaving loop block, fix `break` and `continue` Jumps
    fn pop_loop_block(&mut self, icontinue: usize) {
        // breaks
        let iend = self.fp.byte_codes.len() - 1;
        for i in self.break_blocks.pop().unwrap().into_iter() {
            self.fp.byte_codes[i] = ByteCode::Jump((iend - i) as i16);
        }

        // continues
        let end_nvar = self.local_num();
        for (i, i_nvar) in self.continue_blocks.pop().unwrap().into_iter() {
            if i_nvar < end_nvar {
                panic!("continue jump into local scope");
            }
            self.fp.byte_codes[i] = ByteCode::Jump((icontinue as isize - i as isize) as i16 - 1);
        }
    }

    // BNF:
    //   do block end
    fn do_stat(&mut self) {
        assert_eq!(self.block(), Token::End);
    }

    // BNF:
    //   label ::= `::` Name `::`
    fn label_stat(&mut self, igoto: usize) {
        let name = self.read_name();
        self.ctx.lex.expect(Token::DoubColon);

        // check if this label is at the end of block.
        // ignore void statments: `;` and label.
        let is_last = loop {
            match self.ctx.lex.peek() {
                Token::SemiColon => {
                    self.ctx.lex.next();
                }
                Token::DoubColon => {
                    self.ctx.lex.next();
                    self.label_stat(igoto);
                }
                t => break is_block_end(t),
            }
        };

        // check duplicate
        if self.labels.iter().any(|l|l.name == name) {
            panic!("duplicate label {name}");
        }

        let icode = self.fp.byte_codes.len();
        let nvar = self.local_num();

        // match previous gotos
        let mut no_dsts = Vec::new();
        for goto in self.gotos.drain(igoto..) {
            if goto.name == name {
                if !is_last && goto.nvar < nvar {
                    panic!("goto jump into scope {}", goto.name);
                }
                let dist = icode - goto.icode;
                self.fp.byte_codes[goto.icode] = ByteCode::Jump(dist as i16 - 1);
            } else {
                // no matched label
                no_dsts.push(goto);
            }
        }
        self.gotos.append(&mut no_dsts);

        // save the label for following gotos
        self.labels.push(GotoLabel { name, icode, nvar });
    }

    // BNF:
    //   goto Name
    fn goto_stat(&mut self) {
        let name = self.read_name();

        // match previous label
        if let Some(label) = self.labels.iter().rev().find(|l|l.name == name) {
            // find label
            let dist = self.fp.byte_codes.len() - label.icode;
            self.local_check_close(label.nvar);
            self.fp.byte_codes.push(ByteCode::Jump(-(dist as i16) - 1));

        } else {
            // not find label, push a fake byte code and save the goto
            self.fp.byte_codes.push(ByteCode::Jump(0));

            self.gotos.push(GotoLabel {
                name,
                icode: self.fp.byte_codes.len() - 1,
                nvar: self.local_num(),
            });
        }
    }

    // BNF:
    //   retstat ::= return [explist] [‘;’]
    fn ret_stat(&mut self) {
        let code = match self.ctx.lex.peek() {
            Token::SemiColon => {
                self.ctx.lex.next();
                ByteCode::Return0
            }
            t if is_block_end(t) => {
                ByteCode::Return0
            }
            _ => { // return values
                let iret = self.sp;
                let (nexp, last_exp) = self.explist();

                // check optional ';'
                if self.ctx.lex.peek() == &Token::SemiColon {
                    self.ctx.lex.next();
                }
                // check block end
                if !is_block_end(self.ctx.lex.peek()) {
                    panic!("'end' expected");
                }

                if let (0, &ExpDesc::Local(i)) = (nexp, &last_exp) {
                    // only 1 return value, so NOT need discharging all values to
                    // stack top for continuity
                    ByteCode::Return(i as u8, 1)

                } else if let (0, &ExpDesc::Call(func, narg_plus)) = (nexp, &last_exp) {
                    // tail call
                    ByteCode::TailCall(func as u8, narg_plus as u8)

                } else if self.discharge_try_expand(last_exp, 0) {
                    // return variable values
                    ByteCode::Return(iret as u8, 0)

                } else {
                    // return fixed values
                    ByteCode::Return(iret as u8, nexp as u8 + 1)
                }
            }
        };
        self.fp.byte_codes.push(code);
    }

    // process assignment: var = value
    fn assign_var(&mut self, var: ExpDesc, value: ExpDesc) {
        if let ExpDesc::Local(i) = var {
            // self.sp will be set to i+1 in self.discharge(), which is
            // NOT expected, but it's ok because self.sp will not be used
            // before next statement.
            self.discharge(i, value);
        } else {
            match self.discharge_const(value) {
                ConstStack::Const(i) => self.assign_from_const(var, i),
                ConstStack::Stack(i) => self.assign_from_stack(var, i),
            }
        }
    }

    fn assign_from_stack(&mut self, var: ExpDesc, value: usize) {
        let code = match var {
            ExpDesc::Local(i) => ByteCode::Move(i as u8, value as u8),
            ExpDesc::Upvalue(i) => ByteCode::SetUpvalue(i as u8, value as u8),
            ExpDesc::Index(t, key) => ByteCode::SetTable(t as u8, key as u8, value as u8),
            ExpDesc::IndexField(t, key) => ByteCode::SetField(t as u8, key as u8, value as u8),
            ExpDesc::IndexInt(t, key) => ByteCode::SetInt(t as u8, key, value as u8),
            ExpDesc::IndexUpField(t, key) => ByteCode::SetUpField(t as u8, key as u8, value as u8),
            _ => panic!("assign from stack"),
        };
        self.fp.byte_codes.push(code);
    }

    fn assign_from_const(&mut self, var: ExpDesc, value: usize) {
        let code = match var {
            ExpDesc::Upvalue(i) => ByteCode::SetUpvalueConst(i as u8, value as u8),
            ExpDesc::Index(t, key) => ByteCode::SetTableConst(t as u8, key as u8, value as u8),
            ExpDesc::IndexField(t, key) => ByteCode::SetFieldConst(t as u8, key as u8, value as u8),
            ExpDesc::IndexInt(t, key) => ByteCode::SetIntConst(t as u8, key, value as u8),
            ExpDesc::IndexUpField(t, key) => ByteCode::SetUpFieldConst(t as u8, key as u8, value as u8),
            _ => panic!("assign from const"),
        };
        self.fp.byte_codes.push(code);
    }

    // add the value to constants
    fn add_const(&mut self, c: impl Into<Value>) -> usize {
        let c = c.into();
        let constants = &mut self.fp.constants;
        constants.iter().position(|v| v.same(&c)).unwrap_or_else(|| {
            constants.push(c);
            constants.len() - 1
        })
    }

    // explist ::= exp {`,` exp}
    //
    // Read expressions, discharge front ones, and keep last one.
    // Return the number of front expressions and the last expression.
    fn explist(&mut self) -> (usize, ExpDesc) {
        let sp0 = self.sp;
        let mut n = 0;
        loop {
            let desc = self.exp();
            if self.ctx.lex.peek() != &Token::Comma {
                self.sp = sp0 + n;
                return (n, desc);
            }
            self.ctx.lex.next();

            self.discharge(sp0 + n, desc);
            n += 1;
        }
    }

    fn explist_want(&mut self, want: usize) {
        let (nexp, last_exp) = self.explist();
        match (nexp + 1).cmp(&want) {
            Ordering::Equal => {
                self.discharge(self.sp, last_exp);
            }
            Ordering::Less => {
                // expand last expressions
                self.discharge_expand_want(last_exp, want - nexp);
            }
            Ordering::Greater => {
                // drop extra expressions
                self.sp -= nexp - want;
            }
        }
    }

    // BNF:
    //   exp ::= nil | false | true | Numeral | LiteralString | `...` | functiondef |
    //           prefixexp | tableconstructor | exp binop exp | unop exp
    //
    // Remove left recursion:
    //
    //   exp ::= (nil | false | true | Numeral | LiteralString | `...` | functiondef |
    //           prefixexp | tableconstructor | unop exp) A'
    // where:
    //   A' ::= binop exp A' | Epsilon
    fn exp(&mut self) -> ExpDesc {
        self.exp_limit(0)
    }
    fn exp_limit(&mut self, limit: i32) -> ExpDesc {
        let ahead = self.ctx.lex.next();
        self.do_exp(limit, ahead)
    }
    fn exp_with_ahead(&mut self, ahead: Token) -> ExpDesc {
        self.do_exp(0, ahead)
    }
    fn do_exp(&mut self, limit: i32, ahead: Token) -> ExpDesc {
        // beta
        let mut desc = match ahead {
            Token::Nil => ExpDesc::Nil,
            Token::True => ExpDesc::Boolean(true),
            Token::False => ExpDesc::Boolean(false),
            Token::Integer(i) => ExpDesc::Integer(i),
            Token::Float(f) => ExpDesc::Float(f),
            Token::String(s) => ExpDesc::String(s),

            Token::Dots => {
                if !self.fp.has_varargs {
                    panic!("no varargs");
                }
                ExpDesc::VarArgs
            }
            Token::Function => self.funcbody(false),
            Token::CurlyL => self.table_constructor(),

            Token::Sub => self.unop_neg(),
            Token::Not => self.unop_not(),
            Token::BitNot => self.unop_bitnot(),
            Token::Len => self.unop_len(),

            t => self.prefixexp(t),
        };

        // A' = alpha A'
        loop {
            // Expand only if next operator has priority higher than 'limit'.
            // Non-operator tokens' priority is -1(lowest) so they always break here.
            let (left_pri, right_pri) = binop_pri(self.ctx.lex.peek());
            if left_pri <= limit {
                return desc;
            }

            let binop = self.ctx.lex.next();
            desc = self.preprocess_binop_left(desc, &binop);
            let right_desc = self.exp_limit(right_pri);
            desc = self.process_binop(binop, desc, right_desc);
        }
    }

    // used for unary operand
    fn exp_unop(&mut self) -> ExpDesc {
        self.exp_limit(12) // 12 is all unary operators' priority
    }

    // BNF:
    //   prefixexp ::= var | functioncall | `(` exp `)`
    //   var ::=  Name | prefixexp `[` exp `]` | prefixexp `.` Name
    //   functioncall ::=  prefixexp args | prefixexp `:` Name args
    //
    // We need to remove left recursion amount these 3 rules.
    //
    // First unfold 'var' and 'functioncall' in 'prefixexp' to remove indirect recursion:
    //
    //   prefixexp ::= Name | prefixexp `[` exp `]` | prefixexp `.` Name | prefixexp args | prefixexp `:` Name args | `(` exp `)`
    //
    // Then remove the direct left recursion following:
    //   A ::= A alpha | beta
    // into
    //   A ::= beta A'
    //   A' ::= alpha A' | Epsilon
    //
    // so
    //   prefixexp ::= prefixexp (`[` exp `]` | `.` Name | args | `:` Name args) | Name | `(` exp `)`
    //               = prefixexp alpha | beta
    // where
    //   alpha ::= `[` exp `]` | `.` Name | args | `:` Name args
    //   beta ::= Name | `(` exp `)`
    //
    // Finally we get:
    //   prefixexp ::= beta A'
    //               = (Name | `(` exp `)`) A'
    // where:
    //   A' ::= alpha A' | Epsilon
    //        = (`[` exp `]` | `.` Name | args | `:` Name args) A' | Epsilon
    fn prefixexp(&mut self, ahead: Token) -> ExpDesc {
        let sp0 = self.sp;

        // beta
        let mut desc = match ahead {
            Token::Name(name) => self.simple_name(name),
            Token::ParL => { // `(` exp `)`
                let desc = self.exp();
                self.ctx.lex.expect(Token::ParR);
                desc
            }
            t => panic!("invalid prefixexp {t:?}"),
        };

        // A' = alpha A'
        loop {
            match self.ctx.lex.peek() {
                Token::SqurL => { // `[` exp `]`
                    self.ctx.lex.next();
                    let key = self.exp();
                    self.ctx.lex.expect(Token::SqurR);

                    desc = match (desc, key) {
                        // special case: upvalue-table and string-key
                        (ExpDesc::Upvalue(itable), ExpDesc::String(key)) => {
                            ExpDesc::IndexUpField(itable, self.add_const(key))
                        }
                        // normal case
                        (table, key) => {
                            let itable = self.discharge_if_need(sp0, table);
                            match key {
                                ExpDesc::String(key) =>
                                    ExpDesc::IndexField(itable, self.add_const(key)),
                                ExpDesc::Integer(i) if u8::try_from(i).is_ok() =>
                                    ExpDesc::IndexInt(itable, u8::try_from(i).unwrap()),
                                _ =>
                                    ExpDesc::Index(itable, self.discharge_any(key)),
                            }
                        }
                    };
                }
                Token::Dot => { // .Name
                    self.ctx.lex.next();
                    let name = self.read_name();
                    let ikey = self.add_const(name);

                    desc = if let ExpDesc::Upvalue(itable) = desc {
                        ExpDesc::IndexUpField(itable, ikey)
                    } else {
                        let itable = self.discharge_if_need(sp0, desc);
                        ExpDesc::IndexField(itable, ikey)
                    };
                }
                Token::Colon => { // :Name args
                    self.ctx.lex.next();
                    let name = self.read_name();
                    let ikey = self.add_const(name);
                    let itable = self.discharge_if_need(sp0, desc);

                    // GetFieldSelf:
                    //   stack[sp0] := itable[ikey]  # load function
                    //   stack[sp0+1] := itable      # load table as first argument
                    self.fp.byte_codes.push(
                        ByteCode::GetFieldSelf(sp0 as u8, itable as u8, ikey as u8));

                    // discharge following arguments begin at sp0+2
                    self.sp = sp0 + 2;

                    desc = self.args(1);
                }
                Token::ParL | Token::CurlyL | Token::String(_) => { // args
                    self.discharge(sp0, desc);
                    desc = self.args(0);
                }
                _ => return desc, // Epsilon
            }
        }
    }

    fn local_num(&self) -> usize {
        self.ctx.levels.last().unwrap().locals.len()
    }

    fn local_new(&mut self, name: String) {
        self.ctx.levels.last_mut().unwrap().locals.push((name, false));
    }

    fn local_expire(&mut self, from: usize) {
        // drop locals
        let mut vars = self.ctx.levels.last_mut().unwrap().locals.drain(from..);

        // generate Close if any dropped local variable referred as upvalue
        if vars.any(|v| v.1) {
            self.fp.byte_codes.push(ByteCode::Close(from as u8));
        }
    }

    // generate Close if any local variable in [from..] referred as upvalue
    fn local_check_close(&mut self, from: usize) {
        let mut vars = self.ctx.levels.last().unwrap().locals[from..].iter();
        if vars.any(|v| v.1) {
            self.fp.byte_codes.push(ByteCode::Close(from as u8));
        }
    }

    // match the name as local, upvalue, or global
    fn simple_name(&mut self, name: String) -> ExpDesc {
        let mut level_iter = self.ctx.levels.iter_mut().rev();

        // search from locals and upvalues in current level
        let level = level_iter.next().unwrap();
        if let Some(i) = level.locals.iter().rposition(|v| v.0 == name) {
            // search reversely, so new variable covers old one with same name
            return ExpDesc::Local(i);
        }
        if let Some(i) = level.upvalues.iter().position(|v| v.0 == name) {
            return ExpDesc::Upvalue(i);
        }

        // search in upper levels
        for (depth, level) in level_iter.enumerate() {
            if let Some(i) = level.locals.iter().rposition(|v| v.0 == name) {
                level.locals[i].1 = true; // mark it referred as upvalue
                return self.create_upvalue(name, UpIndex::Local(i), depth);
            }
            if let Some(i) = level.upvalues.iter().position(|v| v.0 == name) {
                return self.create_upvalue(name, UpIndex::Upvalue(i), depth);
            }
        }

        // not matched as local or upvalue, so global variable, by _ENV[name]
        let iname = self.add_const(name);
        match self.simple_name("_ENV".into()) {
            ExpDesc::Local(i) => ExpDesc::IndexField(i, iname),
            ExpDesc::Upvalue(i) => ExpDesc::IndexUpField(i, iname),
            _ => panic!("no here"), // because "_ENV" must exist!
        }
    }

    fn create_upvalue(&mut self, name: String, mut upidx: UpIndex, depth: usize) -> ExpDesc {
        let levels = &mut self.ctx.levels;
        let last = levels.len() - 1;

        // create upvalue in middle levels, if any
        for Level { upvalues, .. } in levels[last-depth .. last].iter_mut() {
            upvalues.push((name.clone(), upidx));
            upidx = UpIndex::Upvalue(upvalues.len() - 1);
        }

        // create upvalue in current level
        let upvalues = &mut levels[last].upvalues;
        upvalues.push((name, upidx));
        ExpDesc::Upvalue(upvalues.len() - 1)
    }

    // unop `-`
    fn unop_neg(&mut self) -> ExpDesc {
        match self.exp_unop() {
            ExpDesc::Integer(i) => ExpDesc::Integer(-i),
            ExpDesc::Float(f) => ExpDesc::Float(-f),
            ExpDesc::Nil | ExpDesc::Boolean(_) | ExpDesc::String(_) => panic!("invalid - operator"),
            desc => ExpDesc::UnaryOp(ByteCode::Neg, self.discharge_any(desc))
        }
    }

    // unop `not`
    fn unop_not(&mut self) -> ExpDesc {
        match self.exp_unop() {
            ExpDesc::Nil => ExpDesc::Boolean(true),
            ExpDesc::Boolean(b) => ExpDesc::Boolean(!b),
            ExpDesc::Integer(_) | ExpDesc::Float(_) | ExpDesc::String(_) => ExpDesc::Boolean(false),
            desc => ExpDesc::UnaryOp(ByteCode::Not, self.discharge_any(desc)),
        }
    }
    // unop `~`
    fn unop_bitnot(&mut self) -> ExpDesc {
        match self.exp_unop() {
            ExpDesc::Integer(i) => ExpDesc::Integer(!i),
            ExpDesc::Nil | ExpDesc::Boolean(_) | ExpDesc::Float(_) | ExpDesc::String(_) => panic!("invalid ~ operator"),
            desc => ExpDesc::UnaryOp(ByteCode::BitNot, self.discharge_any(desc)),
        }
    }
    // unop `#`
    fn unop_len(&mut self) -> ExpDesc {
        match self.exp_unop() {
            ExpDesc::String(s) => ExpDesc::Integer(s.len() as i64),
            ExpDesc::Nil | ExpDesc::Boolean(_) | ExpDesc::Integer(_) | ExpDesc::Float(_) => panic!("invalid ~ operator"),
            desc => ExpDesc::UnaryOp(ByteCode::Len, self.discharge_any(desc)),
        }
    }

    fn preprocess_binop_left(&mut self, left: ExpDesc, binop: &Token) -> ExpDesc {
        // Generate TestOrJump/TestAndJump before reading right operand,
        // because of short-circuit evaluation.
        if binop == &Token::And {
            ExpDesc::Test(Box::new(ExpDesc::Nil), Vec::new(), self.test_or_jump(left))
        } else if binop == &Token::Or {
            ExpDesc::Test(Box::new(ExpDesc::Nil), self.test_and_jump(left), Vec::new())

        // Discharge left operand before reading right operand, which may
        // affect the evaluation of left operand. e.g. `t.k + f(t) * 1`,
        // the `f(t)` may change `t.k`, so we must evaluate `t.k` before
        // calling `f(t)`. */
        // But we do not discharge constants, because they will not be
        // affected by right operand. Besides we try to fold constants
        // in process_binop() later.
        } else if matches!(left, ExpDesc::Integer(_) | ExpDesc::Float(_) | ExpDesc::String(_)) {
            left
        } else {
            ExpDesc::Local(self.discharge_any(left))
        }
    }

    fn process_binop(&mut self, binop: Token, left: ExpDesc, right: ExpDesc) -> ExpDesc {
        if let Some(r) = fold_const(&binop, &left, &right) {
            return r;
        }

        match binop {
            Token::Add => self.do_binop(left, right, ByteCode::Add, ByteCode::AddInt, ByteCode::AddConst),
            Token::Sub => self.do_binop(left, right, ByteCode::Sub, ByteCode::SubInt, ByteCode::SubConst),
            Token::Mul => self.do_binop(left, right, ByteCode::Mul, ByteCode::MulInt, ByteCode::MulConst),
            Token::Mod => self.do_binop(left, right, ByteCode::Mod, ByteCode::ModInt, ByteCode::ModConst),
            Token::Idiv => self.do_binop(left, right, ByteCode::Idiv, ByteCode::IdivInt, ByteCode::IdivConst),
            Token::Div => self.do_binop(left, right, ByteCode::Div, ByteCode::DivInt, ByteCode::DivConst),
            Token::Pow => self.do_binop(left, right, ByteCode::Pow, ByteCode::PowInt, ByteCode::PowConst),
            Token::BitAnd => self.do_binop(left, right, ByteCode::BitAnd, ByteCode::BitAndInt, ByteCode::BitAndConst),
            Token::BitNot => self.do_binop(left, right, ByteCode::BitXor, ByteCode::BitXorInt, ByteCode::BitXorConst),
            Token::BitOr  => self.do_binop(left, right, ByteCode::BitOr, ByteCode::BitOrInt, ByteCode::BitOrConst),
            Token::ShiftL => self.do_binop(left, right, ByteCode::ShiftL, ByteCode::ShiftLInt, ByteCode::ShiftLConst),
            Token::ShiftR => self.do_binop(left, right, ByteCode::ShiftR, ByteCode::ShiftRInt, ByteCode::ShiftRConst),

            Token::Equal => self.do_compare(left, right, ByteCode::Equal, ByteCode::EqualInt, ByteCode::EqualConst),
            Token::NotEq => self.do_compare(left, right, ByteCode::NotEq, ByteCode::NotEqInt, ByteCode::NotEqConst),
            Token::LesEq => self.do_compare(left, right, ByteCode::LesEq, ByteCode::LesEqInt, ByteCode::LesEqConst),
            Token::GreEq => self.do_compare(left, right, ByteCode::GreEq, ByteCode::GreEqInt, ByteCode::GreEqConst),
            Token::Less => self.do_compare(left, right, ByteCode::Less, ByteCode::LessInt, ByteCode::LessConst),
            Token::Greater => self.do_compare(left, right, ByteCode::Greater, ByteCode::GreaterInt, ByteCode::GreaterConst),

            Token::Concat => {
                // TODO support multiple operants
                let left = self.discharge_any(left);
                let right = self.discharge_any(right);
                ExpDesc::BinaryOp(ByteCode::Concat, left, right)
            }

            Token::And | Token::Or => {
                // left operand has been made into ExpDesc::Test in preprocess_binop_left()
                let ExpDesc::Test(_, mut left_true_list, mut left_false_list) = left else {
                    panic!("impossible");
                };
                match right {
                    ExpDesc::Compare(op, l, r, mut right_true_list, mut right_false_list) => {
                        left_true_list.append(&mut right_true_list);
                        left_false_list.append(&mut right_false_list);
                        ExpDesc::Compare(op, l, r, left_true_list, left_false_list)
                    }
                    ExpDesc::Test(condition, mut right_true_list, mut right_false_list) => {
                        left_true_list.append(&mut right_true_list);
                        left_false_list.append(&mut right_false_list);
                        ExpDesc::Test(condition, left_true_list, left_false_list)
                    }
                    _ => ExpDesc::Test(Box::new(right), left_true_list, left_false_list),
                }
            }
            _ => panic!("impossible"),
        }
    }

    fn do_binop(&mut self, mut left: ExpDesc, mut right: ExpDesc,
            opr: FnBc3u8, opi: FnBc3u8, opk: FnBc3u8) -> ExpDesc {

        if opr == ByteCode::Add || opr == ByteCode::Mul { // commutative
            if matches!(left, ExpDesc::Integer(_) | ExpDesc::Float(_)) {
                // swap the left-const-operand to right, in order to use opi/opk
                (left, right) = (right, left);
            }
        }

        let left = self.discharge_any(left);

        let (op, right) = match right {
            ExpDesc::Integer(i) =>
                if let Ok(i) = u8::try_from(i) {
                    (opi, i as usize)
                } else {
                    (opk, self.add_const(i))
                }
            ExpDesc::Float(f) => (opk, self.add_const(f)),
            _ => (opr, self.discharge_any(right)),
        };

        ExpDesc::BinaryOp(op, left, right)
    }

    fn do_compare(&mut self, mut left: ExpDesc, mut right: ExpDesc,
            opr: FnBcBool, opi: FnBcBool, opk: FnBcBool) -> ExpDesc {

        if opr == ByteCode::Equal || opr == ByteCode::NotEq { // commutative
            if matches!(left, ExpDesc::Integer(_) | ExpDesc::Float(_)) {
                // swap the left-const-operand to right, in order to use opi/opk
                (left, right) = (right, left);
            }
        }

        let left = self.discharge_any(left);

        let (op, right) = match right {
            ExpDesc::Integer(i) =>
                if let Ok(i) = u8::try_from(i) {
                    (opi, i as usize)
                } else {
                    (opk, self.add_const(i))
                }
            ExpDesc::Float(f) => (opk, self.add_const(f)),
            ExpDesc::String(s) => (opk, self.add_const(s)),
            _ => (opr, self.discharge_any(right)),
        };

        ExpDesc::Compare(op, left, right, Vec::new(), Vec::new())
    }

    // Generate a TestOrJump: test @condition or jump to somewhere unknown.
    // Link the new code to previous false-list if any.
    // Close true-list if any.
    // Return false-list to be fixed later in fix_test_list()
    fn test_or_jump(&mut self, condition: ExpDesc) -> Vec<usize> {
        let (code, true_list, mut false_list) = match condition {
            ExpDesc::Boolean(true) | ExpDesc::Integer(_) | ExpDesc::Float(_) | ExpDesc::String(_) => {
                // always true, no need to test or jump, e.g. `while true do ... end`
                return Vec::new();
            }
            ExpDesc::Compare(op, left, right, true_list, false_list) => {
                self.fp.byte_codes.push(op(left as u8, right as u8, true));
                (ByteCode::Jump(0), Some(true_list), false_list)
            }
            ExpDesc::Test(condition, true_list, false_list) => {
                let icondition = self.discharge_any(*condition);
                (ByteCode::TestOrJump(icondition as u8, 0), Some(true_list), false_list)
            }
            _ => {
                let icondition = self.discharge_any(condition);
                (ByteCode::TestOrJump(icondition as u8, 0), None, Vec::new())
            }
        };

        self.fp.byte_codes.push(code);

        false_list.push(self.fp.byte_codes.len() - 1);

        if let Some(true_list) = true_list {
            // close true_list to jump here, after TestOrJump
            self.fix_test_list(true_list);
        }

        false_list
    }

    // see test_or_jump()
    fn test_and_jump(&mut self, condition: ExpDesc) -> Vec<usize> {
        let (code, mut true_list, false_list) = match condition {
            ExpDesc::Boolean(false) | ExpDesc::Nil => {
                // always false, no need to test or jump, but I don't know any useful case
                return Vec::new();
            }
            ExpDesc::Compare(op, left, right, true_list, false_list) => {
                self.fp.byte_codes.push(op(left as u8, right as u8, false));
                (ByteCode::Jump(0), true_list, Some(false_list))
            }
            ExpDesc::Test(condition, true_list, false_list) => {
                let icondition = self.discharge_any(*condition);
                (ByteCode::TestAndJump(icondition as u8, 0), true_list, Some(false_list))
            }
            _ => {
                let icondition = self.discharge_any(condition);
                (ByteCode::TestAndJump(icondition as u8, 0), Vec::new(), None)
            }
        };

        self.fp.byte_codes.push(code);

        true_list.push(self.fp.byte_codes.len() - 1);

        if let Some(false_list) = false_list {
            // close false_list to jump here, after TestAndJump
            self.fix_test_list(false_list);
        }

        true_list
    }

    // fix TestAndJump/TestOrJump list to jump to current place
    fn fix_test_list(&mut self, list: Vec<usize>) {
        let here = self.fp.byte_codes.len();
        self.fix_test_list_to(list, here);
    }

    // fix TestAndJump/TestOrJump list to jump to $to
    fn fix_test_list_to(&mut self, list: Vec<usize>, to: usize) {
        for i in list.into_iter() {
            let jmp = (to as isize - i as isize - 1) as i16;
            let code = match self.fp.byte_codes[i] {
                ByteCode::Jump(0) => ByteCode::Jump(jmp),
                ByteCode::TestOrJump(icondition, 0) => ByteCode::TestOrJump(icondition, jmp),
                ByteCode::TestAndJump(icondition, 0) => ByteCode::TestAndJump(icondition, jmp),
                _ => panic!("invalid Test"),
            };
            self.fp.byte_codes[i] = code;
        }
    }

    // fix TestAndJump/TestOrJump list to TestAndSetJump/TestOrSetJump
    fn fix_test_set_list(&mut self, list: Vec<usize>, dst: usize) {
        let here = self.fp.byte_codes.len();
        let dst = dst as u8;
        for i in list.into_iter() {
            let jmp = here - i - 1; // should not be negative
            let code = match self.fp.byte_codes[i] {
                ByteCode::Jump(0) => ByteCode::Jump(jmp as i16),
                ByteCode::TestOrJump(icondition, 0) =>
                    if icondition == dst {
                        ByteCode::TestOrJump(icondition, jmp as i16)
                    } else {
                        ByteCode::TestOrSetJump(dst as u8, icondition, jmp as u8)
                    }
                ByteCode::TestAndJump(icondition, 0) =>
                    if icondition == dst {
                        ByteCode::TestAndJump(icondition, jmp as i16)
                    } else {
                        ByteCode::TestAndSetJump(dst as u8, icondition, jmp as u8)
                    }
                _ => panic!("invalid Test"),
            };
            self.fp.byte_codes[i] = code;
        }
    }

    // args ::= `(` [explist] `)` | tableconstructor | LiteralString
    fn args(&mut self, implicit_argn: usize) -> ExpDesc {
        let ifunc = self.sp - 1 - implicit_argn;
        let narg = match self.ctx.lex.next() {
            Token::ParL => {
                if self.ctx.lex.peek() != &Token::ParR {
                    let (nexp, last_exp) = self.explist();
                    self.ctx.lex.expect(Token::ParR);
                    if self.discharge_try_expand(last_exp, 0) {
                        None // variable arguments
                    } else {
                        Some(nexp + 1)
                    }
                } else {
                    self.ctx.lex.next();
                    Some(0)
                }
            }
            Token::CurlyL => {
                self.table_constructor();
                Some(1)
            }
            Token::String(s) => {
                self.discharge(ifunc+1, ExpDesc::String(s));
                Some(1)
            }
            t => panic!("invalid args {t:?}"),
        };

        // n+1: for fixed #n arguments
        //   0: for variable arguments
        let narg_plus = if let Some(n) = narg { n + implicit_argn + 1 } else { 0 };

        ExpDesc::Call(ifunc, narg_plus)
    }

    // discharge @desc into the top of stack, if need
    fn discharge_any(&mut self, desc: ExpDesc) -> usize {
        let dst = if let &ExpDesc::Call(ifunc, _) = &desc {
            ifunc
        } else {
            self.sp
        };
        self.discharge_if_need(dst, desc)
    }

    // discharge @desc into @dst, if need
    fn discharge_if_need(&mut self, dst: usize, desc: ExpDesc) -> usize {
        if let ExpDesc::Local(i) = desc {
            i // no need
        } else {
            self.discharge(dst, desc);
            dst
        }
    }

    // discharge @desc into @dst, and update self.sp=dst+1
    fn discharge(&mut self, dst: usize, desc: ExpDesc) {
        let code = match desc {
            ExpDesc::Nil => ByteCode::LoadNil(dst as u8, 1),
            ExpDesc::Boolean(b) => ByteCode::LoadBool(dst as u8, b),
            ExpDesc::Integer(i) =>
                if let Ok(i) = i16::try_from(i) {
                    ByteCode::LoadInt(dst as u8, i)
                } else {
                    ByteCode::LoadConst(dst as u8, self.add_const(i) as u16)
                }
            ExpDesc::Float(f) => ByteCode::LoadConst(dst as u8, self.add_const(f) as u16),
            ExpDesc::String(s) => ByteCode::LoadConst(dst as u8, self.add_const(s) as u16),
            ExpDesc::Local(src) =>
                if dst != src {
                    ByteCode::Move(dst as u8, src as u8)
                } else {
                    return;
                }
            ExpDesc::Upvalue(src) => ByteCode::GetUpvalue(dst as u8, src as u8),
            ExpDesc::Index(itable, ikey) => ByteCode::GetTable(dst as u8, itable as u8, ikey as u8),
            ExpDesc::IndexField(itable, ikey) => ByteCode::GetField(dst as u8, itable as u8, ikey as u8),
            ExpDesc::IndexInt(itable, ikey) => ByteCode::GetInt(dst as u8, itable as u8, ikey),
            ExpDesc::IndexUpField(itable, ikey) => ByteCode::GetUpField(dst as u8, itable as u8, ikey as u8),
            ExpDesc::VarArgs => ByteCode::VarArgs(dst as u8, 1),
            ExpDesc::Function(f) => ByteCode::LoadConst(dst as u8, f as u16),
            ExpDesc::Closure(f) => ByteCode::Closure(dst as u8, f as u16),
            ExpDesc::Call(ifunc, narg_plus) => ByteCode::CallSet(dst as u8, ifunc as u8, narg_plus as u8),
            ExpDesc::UnaryOp(op, i) => op(dst as u8, i as u8),
            ExpDesc::BinaryOp(op, left, right) => op(dst as u8, left as u8, right as u8),
            ExpDesc::Test(condition, true_list, false_list) => {
                // fix TestSet list after discharging
                self.discharge(dst, *condition);
                self.fix_test_set_list(true_list, dst);
                self.fix_test_set_list(false_list, dst);
                return;
            }
            ExpDesc::Compare(op, left, right, true_list, false_list) => {
                self.fp.byte_codes.push(op(left as u8, right as u8, false));
                self.fp.byte_codes.push(ByteCode::Jump(1));

                // terminate false-list to SetFalseSkip
                self.fix_test_list(false_list);
                self.fp.byte_codes.push(ByteCode::SetFalseSkip(dst as u8));
                // terminate true-list to LoadBool(true)
                self.fix_test_list(true_list);
                ByteCode::LoadBool(dst as u8, true)
            }
        };
        self.fp.byte_codes.push(code);
        self.sp = dst + 1;
    }

    // for constant types, add @desc to constants;
    // otherwise, discharge @desc into stack
    fn discharge_const(&mut self, desc: ExpDesc) -> ConstStack {
        match desc {
            // add const
            ExpDesc::Nil => ConstStack::Const(self.add_const(())),
            ExpDesc::Boolean(b) => ConstStack::Const(self.add_const(b)),
            ExpDesc::Integer(i) => ConstStack::Const(self.add_const(i)),
            ExpDesc::Float(f) => ConstStack::Const(self.add_const(f)),
            ExpDesc::String(s) => ConstStack::Const(self.add_const(s)),
            ExpDesc::Function(f) => ConstStack::Const(f),

            // discharge to stack
            _ => ConstStack::Stack(self.discharge_any(desc)),
        }
    }

    fn discharge_expand_want(&mut self, desc: ExpDesc, want: usize) {
        debug_assert!(want > 1);
        if !self.discharge_try_expand(desc, want) {
            let code = ByteCode::LoadNil(self.sp as u8, want as u8 - 1);
            self.fp.byte_codes.push(code);
        }
    }

    // try to expand the @desc to #want values.
    // want==0 means expand as many as possible.
    fn discharge_try_expand(&mut self, desc: ExpDesc, want: usize) -> bool {
        match desc {
            ExpDesc::Call(ifunc, narg_plus) => {
                let code = ByteCode::Call(ifunc as u8, narg_plus as u8, want as u8);
                self.fp.byte_codes.push(code);
                true
            }
            ExpDesc::VarArgs => {
                let code = ByteCode::VarArgs(self.sp as u8, want as u8);
                self.fp.byte_codes.push(code);
                true
            }
            _ => {
                self.discharge(self.sp, desc);
                false
            }
        }
    }

    fn table_constructor(&mut self) -> ExpDesc {
        let table = self.sp;
        self.sp += 1;

        let inew = self.fp.byte_codes.len();
        self.fp.byte_codes.push(ByteCode::NewTable(table as u8, 0, 0));

        enum TableEntry {
            Map((FnBc3u8, FnBc3u8, usize)),
            Array(ExpDesc),
        }

        // record the last array entry and do not discharge it immediately,
        // because it may be expanded as varargs or function call.
        let mut last_array_entry = None;

        let mut narray: usize = 0;
        let mut nmap: usize = 0;
        loop {
            let sp0 = self.sp;

            // parse entry of map or array?
            let entry = match self.ctx.lex.peek() {
                Token::CurlyR => { // `}`
                    self.ctx.lex.next();
                    break;
                }
                Token::SqurL => { // `[` exp `]` `=` exp
                    self.ctx.lex.next();

                    let key = self.exp(); // key
                    self.ctx.lex.expect(Token::SqurR); // `]`
                    self.ctx.lex.expect(Token::Assign); // `=`

                    TableEntry::Map(match key {
                        ExpDesc::Local(i) =>
                            (ByteCode::SetTable, ByteCode::SetTableConst, i),
                        ExpDesc::String(s) =>
                            (ByteCode::SetField, ByteCode::SetFieldConst, self.add_const(s)),
                        ExpDesc::Integer(i) if u8::try_from(i).is_ok() =>
                            (ByteCode::SetInt, ByteCode::SetIntConst, i as usize),
                        ExpDesc::Nil =>
                            panic!("nil can not be table key"),
                        ExpDesc::Float(f) if f.is_nan() =>
                            panic!("NaN can not be table key"),
                        _ => (ByteCode::SetTable, ByteCode::SetTableConst, self.discharge_any(key)),
                    })
                }
                Token::Name(_) => {
                    let name = self.read_name();
                    if self.ctx.lex.peek() == &Token::Assign { // Name `=` exp
                        self.ctx.lex.next();
                        TableEntry::Map((ByteCode::SetField, ByteCode::SetFieldConst, self.add_const(name)))
                    } else { // Name
                        TableEntry::Array(self.exp_with_ahead(Token::Name(name)))
                    }
                }
                _ => { // exp
                    TableEntry::Array(self.exp())
                }
            };

            // insert the entry into table
            match entry {
                TableEntry::Map((op, opk, key)) => {
                    let value = self.exp();
                    let code = match self.discharge_const(value) {
                        ConstStack::Const(i) => opk(table as u8, key as u8, i as u8),
                        ConstStack::Stack(i) => op(table as u8, key as u8, i as u8),
                    };
                    self.fp.byte_codes.push(code);

                    nmap += 1;
                    self.sp = sp0;
                }
                TableEntry::Array(desc) => {
                    if let Some(last) = last_array_entry.replace(desc) {
                        self.discharge(sp0, last);

                        narray += 1;
                        if narray % 50 == 0 { // reset the array members every 50
                            self.fp.byte_codes.push(ByteCode::SetList(table as u8, 50));
                            self.sp = table + 1;
                        }
                    }
                }
            }

            // any more entry?
            match self.ctx.lex.next() {
                Token::SemiColon | Token::Comma => (), // yes
                Token::CurlyR => break, // no
                t => panic!("invalid table {t:?}"),
            }
        }

        if let Some(last) = last_array_entry {
            let num = if self.discharge_try_expand(last, 0) {
                // do not update @narray
                0 // 0 is special, means all following values in stack
            } else {
                narray += 1;
                (self.sp - (table + 1)) as u8
            };
            self.fp.byte_codes.push(ByteCode::SetList(table as u8, num));
        }

        // reset narray and nmap
        self.fp.byte_codes[inew] = ByteCode::NewTable(table as u8,
            u8::try_from(narray).unwrap_or(255),
            u8::try_from(nmap).unwrap_or(255));

        self.sp = table + 1;
        ExpDesc::Local(table)
    }

    fn read_name(&mut self) -> String {
        if let Token::Name(name) = self.ctx.lex.next() {
            name
        } else {
            panic!("expect name");
        }
    }
}

pub fn load(input: impl Read) -> FuncProto {
    let mut ctx = ParseContext {
        lex: Lex::new(input),
        levels: Default::default(),
    };
    chunk(&mut ctx, false, vec!["_ENV".into()], Token::Eos) // XXX has_varargs->true
}

fn chunk(ctx: &mut ParseContext<impl Read>, has_varargs: bool, params: Vec<String>, end_token: Token) -> FuncProto {
    // prepare
    let fp = FuncProto {
        has_varargs: has_varargs,
        nparam: params.len(),
        ..Default::default()
    };

    ctx.levels.push(Level {
        locals: params.into_iter().map(|p|(p, false)).collect(),
        upvalues: Vec::new(),
    });

    let mut proto = ParseProto {
        sp: 0,
        break_blocks: Vec::new(),
        continue_blocks: Vec::new(),
        gotos: Vec::new(),
        labels: Vec::new(),

        fp,
        ctx,
    };

    // parse!
    // use `block_scope()` because local variables will be dropped
    // after function, and upvalues will be closed in `Return`
    // byte code.
    assert_eq!(proto.block_scope(), end_token);

    if let Some(goto) = proto.gotos.first() {
        panic!("goto {} no destination", &goto.name);
    }

    // clear
    let ParseProto { mut fp, ctx, ..} = proto;

    let level = ctx.levels.pop().unwrap();
    fp.upindexes = level.upvalues.into_iter().map(|u| u.1).collect();

    fp.byte_codes.push(ByteCode::Return0);

    println!("constants: {:?}", &fp.constants);
    println!("upindexes: {:?}", &fp.upindexes);
    println!("byte_codes:");
    for (i,c) in fp.byte_codes.iter().enumerate() {
        println!("  {i}\t{c:?}");
    }

    fp
}

// priorities of binops
fn binop_pri(binop: &Token) -> (i32, i32) {
    match binop {
        Token::Pow => (14, 13), // right associative
        Token::Mul | Token::Mod | Token::Div | Token::Idiv => (11, 11),
        Token::Add | Token::Sub => (10, 10),
        Token::Concat => (9, 8), // right associative
        Token::ShiftL | Token::ShiftR => (7, 7),
        Token::BitAnd => (6, 6),
        Token::BitNot => (5, 5),
        Token::BitOr => (4, 4),
        Token::Equal | Token::NotEq | Token::Less |
            Token::Greater | Token::LesEq | Token::GreEq => (3, 3),
        Token::And => (2, 2),
        Token::Or => (1, 1),
        _ => (-1, -1)
    }
}

fn is_block_end(t: &Token) -> bool {
    matches!(t, Token::End | Token::Elseif | Token::Else | Token::Until | Token::Eos)
}

fn fold_const(binop: &Token, left: &ExpDesc, right: &ExpDesc) -> Option<ExpDesc> {
    match binop {
        Token::Add => do_fold_const(left, right, |a,b|a+b, |a,b|a+b),
        Token::Sub => do_fold_const(left, right, |a,b|a-b, |a,b|a-b),
        Token::Mul => do_fold_const(left, right, |a,b|a*b, |a,b|a*b),
        Token::Mod => do_fold_const(left, right, |a,b|a%b, |a,b|a%b),
        Token::Idiv => do_fold_const(left, right, |a,b|a/b, |a,b|a/b),

        Token::Div => do_fold_const_float(left, right, |a,b|a/b),
        Token::Pow => do_fold_const_float(left, right, |a,b|a.powf(b)),

        Token::BitAnd => do_fold_const_int(left, right, |a,b|a&b),
        Token::BitNot => do_fold_const_int(left, right, |a,b|a^b),
        Token::BitOr  => do_fold_const_int(left, right, |a,b|a|b),
        Token::ShiftL => do_fold_const_int(left, right, |a,b|a<<b),
        Token::ShiftR => do_fold_const_int(left, right, |a,b|a>>b),

        Token::Concat => {
            if let (ExpDesc::String(s1), ExpDesc::String(s2)) = (left, right) {
                Some(ExpDesc::String([s1.as_slice(), s2.as_slice()].concat()))
            } else {
                None
            }
        }

        _ => None,
    }
}

fn do_fold_const(left: &ExpDesc, right: &ExpDesc, arith_i: fn(i64,i64)->i64, arith_f: fn(f64,f64)->f64) -> Option<ExpDesc> {
    match (left, right) {
        (&ExpDesc::Integer(i1), &ExpDesc::Integer(i2)) => Some(ExpDesc::Integer(arith_i(i1, i2))),
        (&ExpDesc::Float(f1), &ExpDesc::Float(f2)) => Some(ExpDesc::Float(arith_f(f1, f2))),
        (&ExpDesc::Float(f1), &ExpDesc::Integer(i2)) => Some(ExpDesc::Float(arith_f(f1, i2 as f64))),
        (&ExpDesc::Integer(i1), &ExpDesc::Float(f2)) => Some(ExpDesc::Float(arith_f(i1 as f64, f2))),
        (_, _) => None,
    }
}

fn do_fold_const_int(left: &ExpDesc, right: &ExpDesc, arith_i: fn(i64,i64)->i64) -> Option<ExpDesc> {
    let (i1, i2) = match (left, right) {
        (&ExpDesc::Integer(i1), &ExpDesc::Integer(i2)) => (i1, i2),
        (&ExpDesc::Float(f1), &ExpDesc::Float(f2)) => (ftoi(f1).unwrap(), ftoi(f2).unwrap()),
        (&ExpDesc::Float(f1), &ExpDesc::Integer(i2)) => (ftoi(f1).unwrap(), i2),
        (&ExpDesc::Integer(i1), &ExpDesc::Float(f2)) => (i1, ftoi(f2).unwrap()),
        (_, _) => return None,
    };
    Some(ExpDesc::Integer(arith_i(i1, i2)))
}

fn do_fold_const_float(left: &ExpDesc, right: &ExpDesc, arith_f: fn(f64,f64)->f64) -> Option<ExpDesc> {
    let (f1, f2) = match (left, right) {
        (&ExpDesc::Integer(i1), &ExpDesc::Integer(i2)) => (i1 as f64, i2 as f64),
        (&ExpDesc::Float(f1), &ExpDesc::Float(f2)) => (f1, f2),
        (&ExpDesc::Float(f1), &ExpDesc::Integer(i2)) => (f1, i2 as f64),
        (&ExpDesc::Integer(i1), &ExpDesc::Float(f2)) => (i1 as f64, f2),
        (_, _) => return None,
    };
    Some(ExpDesc::Float(arith_f(f1, f2)))
}