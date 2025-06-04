# Drug Discovery MCP

[drug-discovery agent](https://github.com/hsr87/drug-discovery-agent?tab=readme-ov-file#features)에서 아래의 MCP server들을 가져왔습니다.

- arXiv (scientific papers)
- PubMed (biomedical literature)
- ChEMBL (bioactive molecules)
- ClinicalTrials.gov (clinical trials)

이 MCP server들은 아래와 같은 파일로 구현됩니다.

- [mcp_server_arxiv.py](./application/mcp_server_arxiv.py): Search and retrieve scientific papers from arXiv
- [mcp_server_chembl.py](./application/mcp_server_chembl.py): Access chemical and bioactivity data from ChEMBL
- [mcp_server_clinicaltrial.py](./application/mcp_server_clinicaltrial.py): Search and analyze clinical trials
- [mcp_server_pubmed.py](./application/mcp_server_pubmed.py): Access biomedical literature from PubMed
