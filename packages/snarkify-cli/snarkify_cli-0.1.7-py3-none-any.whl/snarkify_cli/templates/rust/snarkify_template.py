RUST_PROJECT_TEMPLATE = """use std::io;

use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use snarkify_sdk::prover::ProofHandler;


struct MyProofHandler;

#[derive(Deserialize)]
struct MyInput {
    /// Define your own input fields here.
    public_input: String,
}

#[derive(Serialize)]
struct MyOutput {
    /// Define your own output fields here.
    proof: String,
}

#[async_trait]
impl ProofHandler for MyProofHandler {
    type Input = MyInput;
    type Output = MyOutput;
    type Error = ();

    async fn prove(data: Self::Input) -> Result<Self::Output, Self::Error> {
        /// Add your own proving logic here by consuming MyInput and producing MyOutput.
        let proof = format!("Hello, {}", data.public_input);

        return Ok(MyOutput {
            proof,
        });
    }
}

fn main() -> Result<(), io::Error> {
    snarkify_sdk::run::<MyProofHandler>()
}"""
