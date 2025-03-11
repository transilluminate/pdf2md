## About

This is a small helper script which uses [Docling](https://github.com/DS4SD/docling) to recursively convert pdf files to markdown.

### Suggested use case:

- If you use [Zotero](https://www.zotero.org/) as a reference manager and [Obsidian](https://obsidian.md/) for notes you can connect the two. There's lots of [youtube videos](https://www.youtube.com/watch?v=XY7NfgtnT6A) for this!
- The next step is with generative AI and a local RAG system based on your Zotero references... but the [Obsidian Copilot](https://github.com/logancyang/obsidian-copilot) plugin does not directly index PDF files.
- This is where this helper script comes in!
- It recursively looks through a specified folder and creates companion Markdown files from any valid input file (i.e. PDF, DOCX).
- You can [create a symlink to trick Obsidian into thinking that your Zotero library is 'underneath' that Vault](https://forum.obsidian.md/t/new-plugin-citations-with-zotero/9793/390?u=transilluminate).
- Now when the Obsidian Copilot extension reindexes, it can use these generated Markdown files for reference (it's not perfect).
- All this can be done locally using [ollama](https://ollama.com/) with minimal setup...
