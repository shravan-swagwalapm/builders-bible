<span class="chapter-number">Chapter 0.2</span>

# Setting Up Your Workshop {.chapter-title}

Every craftsperson needs a workshop. A woodworker has a bench, clamps, and saws. A chef has a kitchen with knives, pans, and a stove. A software builder has a **development environment** — a set of tools that work together so you can write, test, and run software.

In this chapter, we'll set up four tools. Each one exists for a specific reason, and by the end, you'll understand not just *how* to install them but *why* they exist.

## Tool 1: VS Code — Your Workbench

**VS Code** (Visual Studio Code) is a **code editor** — a specialized text editor made for writing software. Think of it as Microsoft Word, but for code. It understands programming languages the way Word understands English — it highlights important words, catches errors, suggests corrections, and organizes your work.

> **ANALOGY**: If building software is like cooking, VS Code is your kitchen counter. It's where you lay out your ingredients (files), follow your recipe (code), and see everything at once. You *could* cook on the floor, but a good counter makes everything easier.

VS Code is free, made by Microsoft, and used by more developers than any other editor in the world. It's not the only option — there's Cursor (which adds AI deeply into the editor), Sublime Text (lightweight and fast), and others. We'll use VS Code because it's free, powerful, and works on every operating system.

**Installation:**

1. Open your web browser
2. Search for "VS Code download" — the first result from `code.visualstudio.com` is the official site
3. Download the version for your operating system (Mac, Windows, or Linux)
4. Install it the way you'd install any application (drag to Applications on Mac, run the installer on Windows)

**First launch:**

When you open VS Code for the first time, you'll see a Welcome tab. The interface has four main areas:

- **The Sidebar** (left): Your file explorer. Shows all the files and folders in your project.
- **The Editor** (center): Where you write code. You can have multiple files open in tabs.
- **The Terminal** (bottom): A built-in terminal — the same one we used in Chapter 0.1, but inside VS Code. Press `` Ctrl+` `` (backtick, the key above Tab) to open it.
- **The Activity Bar** (far left): Icons for switching between different views — files, search, extensions, etc.

> **REAL-LIFE**: Every app you use on your phone was probably written in a code editor like this. The Instagram app? Written in a code editor. The WhatsApp messages you send? The code that delivers them was written in a code editor. You're now using the same kind of tool.

**One important extension to install:**

Click the square icon in the Activity Bar (or press `Cmd+Shift+X` on Mac / `Ctrl+Shift+X` on Windows) to open the Extensions panel. Search for and install:

- **Prettier** — automatically formats your code to look clean and consistent. Like auto-correct, but for code formatting.

That's it for now. We'll add more extensions as we need them.

## Tool 2: Git — Your Time Machine

**Git** is **version control** — a system that remembers every change you've ever made to your files, so you can go back in time if something goes wrong.

> **ANALOGY**: You know how Google Docs saves every version of your document, and you can click "Version history" to see what it looked like yesterday, last week, or last month? Git does the same thing for code — but better. Instead of automatic snapshots at random intervals, *you* decide when to save a version and write a note about what changed.

Without Git, software development would be chaos. Imagine 50 people editing the same document simultaneously with no version history. Someone accidentally deletes a paragraph. Someone else rewrites the introduction. Nobody knows who changed what or when. That's what software development was like before Git.

**Linus Torvalds** — the creator of Linux, the operating system that powers every Android phone, 100% of the world's top 500 supercomputers, and most web servers — created Git in 2005. The story goes that he was so frustrated with existing version control tools that he wrote Git in about two weeks. It's now used by virtually every software project on the planet.

**Installation:**

**On Mac:**
Open your terminal and type:

```bash
# This command checks if Git is already installed
git --version
```

If you see a version number, you're done. If Mac asks you to install "Command Line Developer Tools," say yes — this installs Git along with other useful tools.

**On Windows:**
Search for "git download" and install from `git-scm.com`. During installation, accept all the default options.

**Configuration (do this once):**

```bash
# Tell Git your name — this appears in your version history
git config --global user.name "Your Name"

# Tell Git your email — use the same email you'll use for GitHub
git config --global user.email "your.email@example.com"
```

These commands tell Git who you are, so when you save a version (called a **commit**), your name is attached to it. Think of it as signing your work.

## Tool 3: Node.js — The Engine

**Node.js** is a **runtime** — an engine that runs JavaScript code outside of a web browser.

> **ANALOGY**: JavaScript is like a recipe written in a specific language. A web browser (Chrome, Safari, Firefox) is one kitchen where you can cook that recipe — it runs JavaScript to make websites interactive. Node.js is a *second* kitchen, outside the browser, where you can use the same recipe language to build servers, APIs, command-line tools, and more.

Why does this matter? Because JavaScript is the most widely used programming language in the world, and Node.js lets it run everywhere — not just in browsers. The tools we'll use throughout this book (Next.js, npm packages, build systems) all need Node.js to run.

**Installation:**

1. Search for "Node.js download" — go to `nodejs.org`
2. Download the **LTS (Long-Term Support)** version. LTS means "the stable version that won't surprise you." The other option ("Current") has newer features but might have bugs. Always pick LTS
3. Install it like any other application

**Verify it works:**

```bash
# Check that Node.js is installed and show its version
node --version

# Check that npm (Node Package Manager) is installed
# npm is a tool that downloads and manages code libraries — more on this later
npm --version
```

If you see version numbers for both, you're set.

> **INTUITION**: **npm** deserves a moment. It stands for **Node Package Manager**, and it's one of the most important tools in modern software development. Imagine you're building a house. You *could* make every single brick from scratch. Or you could buy bricks from a supplier. npm is the world's largest supplier of code bricks — over 2 million free, ready-to-use code packages. Need a date picker for your website? `npm install react-datepicker`. Need a tool to send emails? `npm install nodemailer`. The entire modern web runs on npm packages stacked on top of each other.

## Tool 4: GitHub — Your Cloud Backup and Portfolio

**GitHub** is where the world stores code. It's Git (version control) in the cloud, plus collaboration tools, plus a social network for developers. Think of it as Google Drive for code, but with the ability to review each other's work, report bugs, and collaborate with strangers across the world.

> **ANALOGY**: If Git is the time machine on your laptop (saving versions locally), GitHub is the cloud backup that also lets other people see and contribute to your work. It's like the difference between saving a Google Doc on your computer vs. sharing it with a link.

Over 100 million developers use GitHub. Every major open-source project lives there: Linux, React (the tool Facebook built for creating user interfaces), TensorFlow (Google's machine learning framework), and millions more.

**Creating your account:**

1. Go to `github.com`
2. Sign up with your email
3. Choose a username you won't be embarrassed by in five years — this becomes your public identity as a builder
4. The free plan gives you unlimited public and private repositories (code projects)

That's all we need for now. We'll use GitHub to store our projects and eventually deploy them to the web.

## Tool 5 (Bonus): Claude Code — Your AI Building Partner

**Claude Code** is an AI-powered coding tool that runs in your terminal. You describe what you want in English, and it writes code, creates files, runs commands, and helps you build things.

This is the tool that makes the rest of this book possible. In Chapter 0.3, you'll use it for the first time.

**Installation:**

```bash
# Install Claude Code globally using npm
npm install -g @anthropic-ai/claude-code
```

The `-g` flag means "install globally" — make this tool available from anywhere on your computer, not just in one project folder.

To use Claude Code, you'll need an Anthropic account. Visit `claude.ai` and sign up. Claude Pro ($20/month) includes Claude Code access.

**Alternative AI tools** (any of these work for this book's exercises):

- **Cursor**: An entire code editor with AI built in. Download from `cursor.com`. Has a free tier.
- **GitHub Copilot**: Lives inside VS Code as an extension. $19/month, or free for students.
- **Gemini CLI**: Google's terminal agent. Open source and free. `npm install -g @anthropic-ai/claude-code` — wait, that's Claude. For Gemini: `npm install -g @anthropic-ai/claude-code` — actually, Gemini CLI installs via `npx @anthropic-ai/claude-code`. Check Google's latest instructions.
- **Codex CLI**: OpenAI's terminal agent. Open source.

We use Claude Code throughout this book because it's what we use in production. Every exercise can be adapted to other tools — when you see "Ask Claude Code to...", you can substitute your tool of choice.

## Your Workshop Is Ready

Let's verify everything works. Open your terminal (or the terminal inside VS Code) and run these commands:

```bash
# Check each tool
git --version      # Should show: git version 2.x.x
node --version     # Should show: v20.x.x or v22.x.x
npm --version      # Should show: 10.x.x or higher
code --version     # Should show: VS Code version (Mac/Linux only)
```

If all four commands show version numbers, your workshop is complete. You have:

| Tool | Purpose | Real-world analogy |
|------|---------|-------------------|
| VS Code | Write and edit code | Your kitchen counter |
| Git | Track every change | Your time machine |
| Node.js | Run JavaScript anywhere | Your engine |
| GitHub | Store code in the cloud | Your cloud backup + portfolio |
| Claude Code | AI building partner | Your experienced co-worker |

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

1. Open VS Code.
2. Press `` Ctrl+` `` to open the integrated terminal.
3. Navigate to your exercises folder: `cd ~/Desktop/builders-bible-exercises`
4. Create a new project folder: `mkdir hello-world && cd hello-world`
5. Initialize a Git repository: `git init`
6. You'll see: `Initialized empty Git repository in .../hello-world/.git/`
7. Type `ls -la` — notice the `.git` folder. This is where Git stores your version history. You never need to touch this folder directly.

You now have a development environment that professional engineers would recognize and respect. The tools are the same. The journey begins here.

</div>

---

**Chapter endnotes**

[1] VS Code was released by Microsoft in 2015 and is itself open source. In the 2024 Stack Overflow Developer Survey, 73% of developers reported using VS Code as their primary editor.

[2] The npm registry at `npmjs.com` contains over 2 million packages. Over 2.1 billion packages are downloaded *per day*. When people say "don't reinvent the wheel," npm is the warehouse where all the pre-made wheels live.

[3] Addy Osmani's "Vibe Coding: The Future of Programming" (O'Reilly, 2025) provides an excellent comparison of the AI coding tool landscape. His framework for choosing between tools based on your workflow preferences influenced our presentation.
