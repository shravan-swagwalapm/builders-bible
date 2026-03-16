<span class="chapter-number">Colophon</span>

# How This Book Was Made {.chapter-title}

This book was written by a human and an AI working in parallel, using the same tools and workflows the book teaches.

**AI Model:** Claude Opus 4.6 by Anthropic, the most capable model available at the time of writing. Every chapter was drafted through conversation: Shravan provided structure, constraints, and editorial direction; Claude generated prose, code examples, and technical explanations. No chapter was accepted on first draft. Most went through three to five revision cycles, each time with sharper constraints and more specific feedback. The prompting patterns described in Chapter 11 were the same patterns used to write Chapter 11.

**Writing Environment:** Claude Code, Anthropic's CLI agent, running in a terminal. The same tool described in Chapter 19. The CLAUDE.md file governing the writing process followed the Advanced template from Appendix B — proof that the templates work for creative projects, not just software.

**Parallel Authoring:** Multiple chapters were written simultaneously using parallel subagent invocations within Claude Code. The chapter dependency graph was mapped before writing began to identify which chapters could be parallelized (Part I and Part II had minimal cross-dependencies) and which required sequential authoring (Part IV references concepts from every earlier part). Cross-references were reconciled in dedicated editing passes.

**Version Control:** Git, hosted on GitHub. Every chapter, every revision, every structural decision tracked in commit history. The repository is a record of how human-AI collaboration actually works in practice: large initial drafts, targeted revisions, occasional complete rewrites when the direction was wrong, and final polishing passes that caught the inconsistencies no single session could see.

**Notes and Planning:** Obsidian, a local-first markdown knowledge base. Chapter outlines, research notes, cross-reference maps, decision logs, and session journals lived in an Obsidian vault structured by the ProductBrain system. Knowledge captured in one writing session was retrievable in every subsequent session.

**PDF Generation:** WeasyPrint, an open-source HTML-to-PDF rendering engine. The book's source files are Markdown, converted to styled HTML with custom CSS for print layout, then rendered to PDF. The design system described in Appendix C was used to style the book itself — the same color tokens, the same typography scale, the same spacing system.

**Typography:** Inter for body text (designed by Rasmus Andersson, optimized for screen readability). JetBrains Mono for code samples (designed for developers, with programming-specific ligatures and clear character distinction). Both are open-source typefaces.

**Diagrams:** ASCII art for all architecture diagrams, ensuring they render correctly in every format: terminal, e-reader, PDF, web browser, and plain text. No external diagramming tools, no image dependencies, no formats that break when the rendering engine changes.

**Code Examples:** Every code sample was tested in the companion repositories. No pseudocode, no "exercise for the reader" shortcuts, no code that compiles but doesn't actually do what the surrounding text claims.

**License:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). You are free to share and adapt this work for any purpose, including commercial use, as long as you give appropriate credit and distribute your contributions under the same license.

**First Edition:** 2026.

**Contact:** For corrections, contributions, and companion repository access, visit the builders-bible GitHub organization.

---

*Built with the tools it teaches. Shipped with the workflows it preaches. Verified with the rigor it demands.*
