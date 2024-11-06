use proc_macro2::TokenStream;
use quote::quote;
use syn::{
    parse_macro_input, parse_str, punctuated::Punctuated, token::Comma, Data, DeriveInput, Fields,
    Ident, Type, Variant,
};

use std::env;
use std::io::Write;
use std::path::PathBuf;
use std::{fs::File, fs::OpenOptions};

fn find_go_file() -> Option<PathBuf> {
    // Get the current working directory
    let current_dir = env::current_dir().expect("Failed to get current directory");

    // Define both potential paths
    let paths = vec![
        current_dir.join("go/generation.go"),
        current_dir.join("../go/generation.go"),
    ];

    // Iterate through the paths and return the first existing one
    for path in paths {
        if path.exists() {
            return Some(path);
        }
    }

    None // Return None if neither path exists
}

fn add_to_file(go_code: &str) {

    match find_go_file() {
        Some(path) => {


    // Create or open the file for appending
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .open(path.clone())
        .unwrap_or_else(|_| {
            // Create the file if it does not exist
            File::create(&path).expect("Unable to create file")
        });

    // Write the generated code to the file
    if let Err(e) = writeln!(file, "{}", go_code) {
        eprintln!("Failed to write to file: {}", e);
    }  
        }
        None => {
            println!("Go file not found in expected locations.");
        }
    }
    

}

fn to_pascal_case(s: &str) -> String {
    s.split('_')
        .map(|word| {
            let mut chars = word.chars();
            match chars.next() {
                None => String::new(),
                Some(first) => {
                    let mut capitalized = first.to_uppercase().to_string();
                    capitalized.push_str(&chars.collect::<String>().to_lowercase());
                    capitalized
                }
            }
        })
        .collect::<String>()
}

#[proc_macro_derive(GoGenerate)]
pub fn go_generate(input: proc_macro::TokenStream) -> proc_macro::TokenStream {  
    // Parse the input tokens into a syntax tree

    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;

    match input.data {
        Data::Struct(data_struct) => generate_go_struct(&name, &data_struct.fields).into(),
        Data::Enum(data_enum) => generate_go_enum(&name, &data_enum.variants).into(),
        _ => unimplemented!("Only structs and enums are supported"),
    }

    //  generate go code and save
}



/// Generates a Go struct from a Rust struct
fn generate_go_struct(name: &Ident, fields: &Fields) -> TokenStream {
    let struct_name = name.to_string();

    let mut go_fields = String::new();

    match fields {
        Fields::Named(fields_named) => {
            for field in &fields_named.named.clone() { 
                let field_name = field.ident.clone().unwrap().to_string();
                let field_type = rust_type_to_go_type(&field.ty);

                //println!("field_name: {}, field_type: {}", field_name, field_type);
                go_fields.push_str(&format!( 
                    "\t{} {} `json:\"{},omitempty\"`\n",
                    to_pascal_case(&field_name),
                    field_type,
                    to_pascal_case(&field_name)
                ));
            }
        }
        Fields::Unnamed(fields_unnamed) => {
            for field in &fields_unnamed.unnamed.clone() {
                let field_type = rust_type_to_go_type(&field.ty);
                
                go_fields.push_str(&format!(
                    "\t{} {} `json:\"{},omitempty\"`\n",
                    to_pascal_case(&field_type),
                    field_type,
                    to_pascal_case(&field_type)
                ));
            }
        }
        _ => (),
    }

    let go_code = format!(
        "type {} struct {{\n\
         {}}}\n",
        struct_name, go_fields
    );

    add_to_file(&go_code);

    let output = quote! {

        impl #name {
            pub fn go_code() -> String {
                #go_code.to_string()
            }
        }
    };

    output.into()
}

/// Generates a Go enum from a Rust enum
fn generate_go_enum(name: &Ident, variants: &Punctuated<Variant, Comma>) -> TokenStream {
    let enum_name = name.to_string();
    let mut go_consts = String::new();
    let mut go_body_types: String = String::new();

    // Generate constant definitions for each variant
    for (i, variant) in variants.iter().enumerate() {
        let variant_name = variant.ident.to_string();

        match &variant.fields {
            Fields::Unit => {
                // Simple enum variant
                go_consts.push_str(&format!("\t{} {} = {}\n", variant_name, enum_name, i));
            }
            Fields::Named(fields) => {
                // Struct-like enum variant
                let mut struct_fields = String::new();
                for field in &fields.named {
                    let field_name = field.ident.clone().unwrap().to_string();
                    let field_type = rust_type_to_go_type(&field.ty);

                    // Convert to PascalCase
                    let go_field_name =
                        format!("{}{}", field_name[..1].to_uppercase(), &field_name[1..]);

                    struct_fields.push_str(&format!("\t{} {}\n", go_field_name, field_type));
                }

                //Generate the struct type and const
                go_consts.push_str(&format!(
                    "\ttype {} struct {{\n{}}}\n",
                    variant_name, struct_fields
                ));
                go_consts.push_str(&format!("\t{} {} = {}\n", variant_name, enum_name, i));
            }
            Fields::Unnamed(fields) => {
                // Tuple-like enum variant
                let field_types: Vec<String> = fields
                    .unnamed
                    .iter()
                    .map(|field| rust_type_to_go_type(&field.ty))
                    .collect();

                // Generate the struct type with numbered fields
                let struct_fields: String = field_types
                    .iter()
                    .enumerate()
                    .map(|(_j, ty)| format!("\t{}\n", ty))
                    .collect();

                let str_struct_field = struct_fields.replace("\n", "").replace("\t", "");

                fn get_go_format_body(str_struct_field: String) -> String {
                    format!("type {} Body \n", str_struct_field)
                }

                match str_struct_field.as_str() {
                    "NotifyProductionTimetable" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    "NotifyEstimatedTimetable" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    "NotifyStopMonitoring" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    "NotifyVechicleMonitoring" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    "NotifyConnectionMonitoring" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    "NotifyGeneralMessage" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    "NotifyFacilityMonitoring" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    "NotifySituationExchange" => {
                        let go_code = get_go_format_body(str_struct_field);
                        go_body_types.push_str(&go_code);
                    }
                    _ => {
                    go_consts.push_str(&format!(
                        "\ttype {} struct {{\n{}}}\n",
                        variant_name, struct_fields
                    ));
                    go_consts.push_str(&format!("\t{} {} = {}\n", variant_name, enum_name, i));
                    }
                }

            }
        }
    }

    let go_code = format!(
        "type {} int\n\n\
         const (\n\
         {})\n",
        enum_name, go_consts
    );

    add_to_file(&go_code);
    add_to_file(&go_body_types);

    let output = quote! {

        impl #name {
            pub fn go_code() -> String {
                #go_code.to_string()
            }
        }
    };

    output.into()
}

/// Derive a go struct from a Rust struct
fn rust_type_to_go_type(ty: &Type) -> String {
    match ty {
        Type::Path(type_path) => {
            let segments = &type_path.path.segments;
            if let Some(segment) = segments.last() {
                let ident = &segment.ident;

                match ident.to_string().as_str() {
                    "i8" => "int8".to_string(),
                    "i16" => "int16".to_string(),
                    "i32" => "int32".to_string(),
                    "i64" => "int64".to_string(),
                    "u8" => "uint8".to_string(),
                    "u16" => "uint16".to_string(),
                    "u32" => "uint32".to_string(),
                    "u64" => "uint64".to_string(),
                    "f32" => "float32".to_string(),
                    "f64" => "float64".to_string(),
                    "bool" => "bool".to_string(),
                    "String" => "string".to_string(),
                    _ if ident == "Vec" => {
                        if let syn::PathArguments::AngleBracketed(args) = &segment.arguments {
                            if let Some(arg) = args.args.first() {
                                return format!(
                                    "[]{}",
                                    rust_type_to_go_type(
                                        &parse_str::<Type>(&quote!(#arg).to_string()).unwrap()
                                    )
                                );
                            }
                        }
                        panic!("Unsupported Vec type");
                    }
                    _ if ident == "Option" => {
                        if let syn::PathArguments::AngleBracketed(args) = &segment.arguments {
                            if let Some(arg) = args.args.first() {
                                return format!(
                                    "*{}",
                                    rust_type_to_go_type(
                                        &parse_str::<Type>(&quote!(#arg).to_string()).unwrap()
                                    )
                                );
                            }
                        }
                        panic!("Unsupported Option type");
                    }
                    _ => {
                        return quote!(#ty).to_string();
                    }
                }
            } else {
                panic!("Unsupported type: {}", quote!(#ty));
            }
        }
        _ => panic!("Unsupported type: {}", quote!(#ty)),
    }
}

#[cfg(test)]
mod tests {
    use crate::GoGenerate;
    use proc_macro2::Span;
    use syn::{
        parse_str, punctuated::Punctuated, token::Comma, Field, Fields, Ident, Token, Type, Variant,
    };

    #[test]
    fn test_rust_type_to_go_type() {
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("i32").unwrap()),
            "int32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("i64").unwrap()),
            "int64"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("u32").unwrap()),
            "uint32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("u64").unwrap()),
            "uint64"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("f32").unwrap()),
            "float32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("f64").unwrap()),
            "float64"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("bool").unwrap()),
            "bool"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("String").unwrap()),
            "string"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("Option<i32>").unwrap()),
            "*int32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("Vec<i32>").unwrap()),
            "[]int32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("Option<Vec<i32>>").unwrap()),
            "*[]int32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("Vec<Vec<i32>>").unwrap()),
            "[][]int32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("Vec<Option<i32>>").unwrap()),
            "[]*int32"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("Vec<Body>").unwrap()),
            "[]Body"
        );
        assert_eq!(
            super::rust_type_to_go_type(&syn::parse_str::<syn::Type>("Vec<Option<Body>>").unwrap()),
            "[]*Body"
        );
    }

    #[test]
    fn test_generate_go_enum() {
        let enum_name = parse_str::<Ident>("MyEnum").unwrap();

        // Parse individual variants
        let variant_names = vec!["Variant1", "Variant2"];
        let variants: Punctuated<Variant, Comma> = variant_names
            .iter()
            .map(|&name| {
                let variant: Variant = parse_str(name).unwrap();
                variant
            })
            .collect();

        let output = super::generate_go_enum(&enum_name, &variants);
        assert_eq!(
            output.to_string(),
            "type MyEnum int\n\nconst (\n\tVariant1 MyEnum = 0\n\tVariant2 MyEnum = 1\n)\n"
        );
    }

    #[test]
    fn test_generate_go_struct() {
        let struct_name = parse_str::<Ident>("MyStruct").unwrap();

        // Create fields manually instead of parsing
        let field_names = vec!["field1", "field2"];
        let field_types = vec!["Option<i32>", "i64"];
        let fields: Fields = {
            let mut fields_vec = vec![];
            for (name, ty) in field_names.iter().zip(field_types.iter()) {
                // Create each field manually
                let field = Field {
                    attrs: vec![],
                    vis: syn::Visibility::Inherited,
                    ident: Some(Ident::new(name, Span::call_site())),
                    colon_token: Some(Token![:](Span::call_site())),
                    ty: parse_str(ty).unwrap(),
                    mutability: syn::FieldMutability::None,
                };
                fields_vec.push(field);
            }
            Fields::Named(syn::FieldsNamed {
                brace_token: Default::default(),
                named: Punctuated::from_iter(fields_vec),
            })
        };

        let output = super::generate_go_struct(&struct_name, &fields);
        assert_eq!(
            output.to_string(),
            "type MyStruct struct {\n\tField1 int32\n\tField2 int64\n}\n"
        );
    }
}
