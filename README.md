# Po_Chat - A Chat Application Built with Django

Po_Chat is a real-time chat application designed and developed using the Django framework. It aims to provide a smooth, secure, and engaging communication platform for users. Whether you're building a small-scale social chat app or integrating chat features into larger projects, LOL_Chat offers a solid foundation to get started.

## Features
- **User Authentication:** Secure user registration, login, and profile management.
- **Real-time Messaging:** Seamless chat experience with instant message delivery.
- **Chat Rooms:** Create or join multiple chat rooms for group conversations.
- **Private Messaging:** One-on-one chats for more personal communication.
- **Responsive Design:** User-friendly interface compatible with desktop and mobile devices.
- **Customizable:** Easily extend or modify the app to fit specific use cases.

## Technologies Used
- **Backend:** Django framework for robust server-side functionality.
- **Database:** SQLite (or easily switch to PostgreSQL, MySQL, etc.).
- **Frontend:** Django templates with responsive design.
- **Real-time Communication:** Django Channels for WebSocket integration.

## How to Use
1. **Clone the repository:**
``bash
https://github.com/soumyajit-ojha/Po_Chat.git``

2. **Navigate to the project directory:**
``bash
cd backend``



### Branching Strategies

When starting new work, always clone the repository and pull the latest changes from the `development` branch. Create your feature or fix branch from `development` to ensure you are working with the most recent codebase.

### Steps:
1. Clone the repository:
    ```bash
    git clone <repo-url>
    ```
2. Checkout the `development` branch and pull latest changes:
    ```bash
    git checkout development
    git pull origin development
    ```
3. Create your new branch from `development`:
    ```bash
    git checkout -b <branch-name>
    ```

### Types of Branches

| Branch Type   | Naming Convention Example           | Purpose                                 |
|---------------|-------------------------------------|-----------------------------------------|
| Feature       | `feature/<short-description>`       | New features or enhancements            |
| Bugfix        | `bugfix/<short-description>`        | Fixing bugs or issues                   |
| Hotfix        | `hotfix/<short-description>`        | Critical fixes for production           |
| Release       | `release/<version-number>`          | Preparing a new production release      |
| Development   | `development`                       | Main integration branch for development |
| Main/Master   | `main` or `master`                  | Production-ready code                   |

**Examples:**
- `feature/user-authentication`
- `bugfix/fix-email-validation`
- `hotfix/critical-payment-bug`
- `release/v1.2.0`

### Commit Message Format

Follow the conventional commit style for clarity and consistency:

```
<type>(<scope>): <short description>

[optional body]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**
- `feat(users): add JWT authentication`
- `fix(payments): resolve rounding error in invoice calculation`
- `docs(readme): update API usage instructions`
- `refactor(core): optimize query performance`
- `style(button): format code according to Prettier rules`
- `test(auth): add unit tests for login flow`
- `chore(deps): upgrade Django to 4.2.1` 