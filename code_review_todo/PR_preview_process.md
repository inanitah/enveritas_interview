# PR Review Process

## Objective

When reviewing a Pull Request (PR), it's important to understand the overall use case and make sure the developer clearly explains what the code is supposed to do. 
The PR description in GitHub should cover:

1. **Objective**: What's the goal of the code?
2. **Context**: Where will the code run? Link to the original task or user story.
3. **Technical Design**: Give a high-level overview of the design and architecture.

## Code Review Focus

### General Comments

Its important to take into consideration this general comments for a Pull Request in production code:
- Testing
- Logging
- Error Handling
- Code Readability
- Validations
- Function Separation
- Python Best Practices(PEP8)

### Context and Constraints

Know who will use this code and the limitations:

- **Microservice or Web Server**: Is this code running in a microservice or a web server?
- **Load and Performance**: How often will this code run each day, and what are the performance expectations?

### Inline Comments

I added my inline comments directly in the `geography.py` file, like you would see in a GitHub PR. I focused only on this file, even though there might be improvements needed in `models.py` as well.

### Improved Version

I've provided an updated version of the code that separates the service layer from the repository layer. This makes the code more modular and easier to test. You can find this version in `geo_map_creator.py`.
