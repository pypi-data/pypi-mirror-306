use go_generation_derive::GoGenerate;

#[derive(GoGenerate)]
pub enum Lala {
    Leverage(Lep),
}

#[derive(GoGenerate)]
pub struct Lep {
    pub fad: String,
}

#[derive(GoGenerate)]
pub struct Testing {
    pub name: String,
    pub typer: Lala,
}

impl Testing {
    pub fn new(name: String) -> Self {
        Self {
            name,
            typer: Lala::Leverage(Lep {
                fad: "ddd".to_string(),
            }),
        }
    }
}

#[test]
fn test_generate_it() {
    let d = Testing::new("this is it".to_string());
    println!("{}", Testing::go_code())
}
