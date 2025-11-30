# Getting Started

Every project needs a solid foundation. This guide outlines the recommended practices and structure for setting up new development projects.

## Project Layout

A well-organized project structure is essential for maintainability and collaboration. Each project should have a clear separation between version-controlled and non-version-controlled directories.

### Directory Structure

Each project should have a base structure that separates concerns:

**Version Controlled Directories:**

- `docs/` - Primary documentation
- `apps/` or `src/` or `app-name`- Application source code
- `tests/` - Test files
- `scripts/` - Utility scripts

**Non-Version Controlled Directories:**

- `.venv/` - Python virtual environment
- `data/` - Local data files
- `logs/` - Application logs
- `.cache/` - Build and cache files
- `node_modules/` - Node.js dependencies (if applicable)

!!! tip "Use .gitignore"

    Ensure your `.gitignore` file properly excludes non-version-controlled directories to prevent accidental commits.

### Best Practices

- Keep application code separate from generated files
- Use consistent naming conventions across projects
- Document the purpose of each top-level directory
- Keep configuration files at the project root

## Documentation

Documentation is a critical part of any project. A well-documented codebase is easier to maintain, onboard new developers, and understand long after it was written.

### Documentation Structure

I generally maintain multiple types of documentation within a project:

- **`docs/`** - Primary project documentation (user guides, API docs, etc.)
- **`notes/`** - Development notes and research
- **`poc/`** - Proof of concept implementations
- **Inline documentation** - Code comments and docstrings

### Centralized Documentation

I maintain a single version-controlled documentation directory that has links from individual projects. This approach provides several benefits:

### Document Organization

As development is often experimental, it's important to keep track of your experiments and research.

**For Notes:**

- Create separate documents by subject area
- Use descriptive filenames
- Organize by topic or date as appropriate

**For Proof of Concepts:**

- Create subdirectories for each proof of concept
- Include appropriate structure if warranted
- Document the purpose and results of each POC
- Keep them separate from production code

!!! tip "Documentation Best Practices"

    - Write documentation as you code, not after
    - Keep documentation close to the code it describes
    - Use clear, concise language
    - Include examples where helpful
    - Update documentation when code changes

## Writing Code

Writing clean, maintainable code requires discipline and the right tools. Modern development practices emphasize code quality, testing, and documentation.

### Code Quality Tools

All code should be linted by the IDE and automated tools:

- **Linters** - Catch syntax errors and style issues
- **Formatters** - Ensure consistent code formatting
- **Type checkers** - Validate type annotations (for typed languages)
- **Static analysis** - Find potential bugs and security issues

!!! success "Automated Quality Checks"

    Set up pre-commit hooks or CI/CD pipelines to automatically run quality checks before code is merged.

### AI-Assisted Development

Assistive AI has become an essential tool in modern development workflows. However, it's important to use AI responsibly and be aware of its limitations.

**Popular AI Tools:**

- **Cursor** - AI-powered code editor
- **GitHub Copilot** - AI pair programmer
- **ChatGPT/Claude** - General-purpose AI assistants

I often use one of three IDEs depending on the task:

- **PyCharm** - For Python-focused development
- **VS Code** - For general-purpose development
- **Cursor** - For AI-assisted development

!!! info "AI Tool Selection"

    I had **Cursor** build the documentation base server with this documentation being added for a more complete example. This was new code and **Cursor** does a great job at tasks like this and also helping refactor applications.

#### Limitations of AI

While AI tools are powerful, they have significant limitations:

!!! warning "System Architecture"

    None of them will lay out a site or app appropriately in my opinion. They use monolithic modules/classes over base classes and separation of concerns generally. They need to be task-driven and guided to build good sites.

**Common AI Issues:**

- Tendency toward monolithic designs without guidance `.cursorrules`
- May optimize things not mentioned request
- Can produce working code that doesn't meet requirements/purpose
- May introduce unexpected side effects

I have had very mixed results on larger designs where things work but not as expected or they decide to help optimize something not mentioned in the prompt. As with all AI, it's getting better exponentially, but heavy testing is needed and review of all changes in critical systems.

!!! danger "Review **ALL** AI Code"

    Think of AI as **pair programming** as defined for agile development. AI will break things: Branch in VCS, have it help and write tests before allowing it to update systems without tests.

**Best Practices for AI-Assisted Development:**

1. Always work in a version-controlled branch
2. Write tests before making changes
3. Review all AI-generated code thoroughly
4. Test changes in isolation
5. Don't accept AI suggestions blindly
6. Understand what the code does before committing

### Inline Documentation and Metadata

Modern development tools rely heavily on inline documentation for introspection and code generation. This means documentation is no longer optional—it's a first-class citizen in your codebase.

**Tools That Use Inline Documentation:**

- **Swagger/OpenAPI** - API documentation generation
- **ReDoc** - Interactive API documentation
- **FastMCP** - Model Context Protocol tools
- **Sphinx** - Python documentation generator
- **JSDoc** - JavaScript documentation
- And many more...

!!! tip "Documentation as Code"

    Your inline documentation is used by great tools that do introspection. This means you need to put as much energy into documentation as coding generally.

#### What to Document

Inline documentation should focus on:

- **WHY** - Why is the code written this way?
  - What problem does it solve?
  - What design decisions were made?
  - What alternatives were considered?
- **WHO** - Who should be consulted for changes?
  - Original author or maintainer
  - Team or individual responsible
  - External dependencies or stakeholders
- **WHAT** - What does the code do?
  - Function signatures and parameters
  - Return values and types
  - Side effects and exceptions
- **HOW** - How does it work?
  - Algorithm explanations
  - Complex logic breakdowns
  - Integration points

!!! note "AI-Generated Documentation"

    AI will often write good documentation with tab assistance, but as with all things AI, you need to review and often add the why, who, and context that AI might miss.

**Documentation Standards:**

- Follow language-specific documentation conventions
- Use consistent formatting
- Include examples for complex functions
- Document edge cases and error conditions
- Keep documentation up-to-date with code changes

## Summary

Building a solid project foundation involves:

1. **Clear project structure** - Separate version-controlled and non-version-controlled directories
2. **Comprehensive documentation** - Multiple documentation types organized appropriately
3. **Code quality** - Linting, formatting, and quality checks
4. **Responsible AI use** - Leverage AI tools while maintaining code quality
5. **Inline documentation** - Document why, who, what, and how

Following these practices will help create maintainable, understandable, and scalable projects.
