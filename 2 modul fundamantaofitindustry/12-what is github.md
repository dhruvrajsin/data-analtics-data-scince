# What is GitHub?

GitHub is a web-based platform for hosting Git repositories. It provides version control, collaboration tools, and project management features for software development. GitHub stores code, tracks changes, supports teams, and integrates with many development workflows.

## Advantages of Using GitHub

- Version control: track changes, restore old versions, and compare history.
- Collaboration: multiple people can work together with pull requests and code reviews.
- Backup: code is stored in a remote repository for safe access.
- Branching: create branches for features or fixes without affecting main code.
- Issue tracking: manage bugs, tasks, and feature requests.
- Documentation: use README, wikis, and markdown files to document projects.
- Integrations: connect with CI/CD, project boards, and third-party tools.
- Community: share open-source projects and discover othersâ€™ code.
- Access control: manage permissions for team members and collaborators.

## Common Git and GitHub Commands

### Git setup and configuration
- `git config --global user.name "Your Name"`
- `git config --global user.email "you@example.com"`

### Repository creation and cloning
- `git init`
- `git clone <repository-url>`

### Checking status and history
- `git status`
- `git log`
- `git diff`

### Staging and committing
- `git add <file>`
- `git add .`
- `git commit -m "message"`

### Branching and merging
- `git branch`
- `git branch <branch-name>`
- `git checkout <branch-name>`
- `git checkout -b <branch-name>`
- `git merge <branch-name>`

### Remote repositories and synchronization
- `git remote add origin <repository-url>`
- `git push origin <branch>`
- `git pull origin <branch>`
- `git fetch`

### Undoing changes
- `git reset --hard <commit>`
- `git reset HEAD <file>`
- `git checkout -- <file>`

### GitHub-specific workflow
- Create a repository on GitHub.
- Push a local repository to GitHub: `git push -u origin main`
- Create a pull request on GitHub.
- Review and merge pull requests in the GitHub web interface.

## Notes

GitHub uses Git commands for version control. The platform adds collaboration, hosting, and project management features on top of Git.
