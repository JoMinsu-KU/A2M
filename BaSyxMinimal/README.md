# 📂 AAS Configuration

This folder contains **Asset Administration Shell (AAS) environment files** used in conjunction with the BaSyxMinimal infrastructure.  
These files describe digital representations of production tools and equipment across various manufacturing processes.

---

## 📌 Context

In the full dataset, a total of **1,005 AAS environment files** were used to represent **25 different manufacturing process types**.  
Each AAS instance provides structured metadata such as tool identifiers (`idShort`) and capability descriptors,  
which are used as input for:

- **LLM-based FastMCP server code generation**
- **Tool discovery by AI agents during orchestration**

> 🔍 This repository only includes the configuration for the `AFPMMotorProductionType` process.  
> This is the **only process tested on a real AFPM manufacturing line**, and thus made publicly available for reference.
- Based on [`BaSyxMinimal`](https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxMinimal)
- Only the contents of this folder (AAS files) were modified — using AFPM-specific templates authored by **Kyungnam University**.
- The rest of the system (AAS Registry, Submodel Repo, Web UI, etc.) follows the BaSyx original setup.
---

## 🧠 Usage Role

Although not a standalone application, this folder acts as an API-like metadata server that enables:

- Retrieval of available tools and submodels
- Support for automated FastMCP code generation by LLMs
- Integration with agent-based control architectures querying the AAS registry

---

## 🪪 License

All AAS files in this directory are provided under the **Apache License 2.0**.  
Please refer to the root [`LICENSE`](../LICENSE) file for full terms.

---

## 📬 Contact

For access to the full set of AAS templates or additional details, please contact:  
**[jms663100@kyungnam.ac.kr](mailto:jms663100@kyungnam.ac.kr)**
