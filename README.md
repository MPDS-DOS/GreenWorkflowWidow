# GreenWorkflowWidow

Representative agentic science workloads for operating-system experiments.
Two open-source agents run against one self-hosted LLM and operate on a shared set of molecules:

- [ChemGraph](chemgraph/) plans and runs short computational-chemistry simulations (ASE, MACE).
- [Biomni](biomni/) writes and executes analysis code against biomedical tools and databases.

The model server is described in [llm/](llm/), benchmark datasets in [datasets/](datasets/),
and the shared example set in [examples/](examples/).
