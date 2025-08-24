# Overview

This is a Flask-based AI routing service that intelligently dispatches user messages to different AI services based on detected tags. The system acts as a message broker, analyzing incoming text for specific tags like `[Io]`, `[Lumo]`, and `[Copilot]` and routing requests to the corresponding AI services (Gemini Oracle, Lumo AI, and GitHub Copilot respectively). The application is designed to be a lightweight middleware layer that simplifies multi-AI integration for users.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Framework
The application is built on Flask, chosen for its simplicity and lightweight nature, making it ideal for a focused API service. The architecture follows a single-responsibility principle where the main purpose is message routing and AI service orchestration.

## Message Processing Pipeline
The system implements a tag-based routing mechanism using regular expressions. Messages are analyzed for specific bracketed tags (`[Io]`, `[Lumo]`, `[Copilot]`) that determine which AI service should handle the request. This pattern-matching approach provides flexibility and makes it easy to add new AI services by simply extending the `TAG_PATTERNS` dictionary.

## AI Service Integration
The architecture uses a placeholder-based approach for AI service integration, with dedicated functions for each service:
- Gemini Oracle (Io) integration via `call_gemini_oracle()`
- Lumo AI integration via `call_lumo_model()`
- GitHub Copilot integration via `call_copilot_service()`

Each service function is designed to handle API key management and service-specific communication protocols.

## Configuration Management
Environment-based configuration is implemented using python-dotenv, allowing secure management of API keys and service credentials. The system provides fallback default values for development environments while maintaining security for production deployments.

## Error Handling and Logging
The application implements comprehensive logging at DEBUG level to facilitate troubleshooting and monitoring of AI service interactions. API keys are partially masked in logs for security purposes.

# External Dependencies

## Core Dependencies
- **Flask**: Web framework for HTTP request handling and API endpoints
- **python-dotenv**: Environment variable management for configuration
- **re**: Built-in regex module for tag pattern matching
- **logging**: Built-in logging module for application monitoring

## AI Service Integrations
- **Gemini API**: Google's Gemini AI service for Oracle (Io) functionality
- **Lumo API**: Custom Lumo AI service integration
- **GitHub Copilot API**: Microsoft's Copilot AI service integration

## Environment Variables Required
- `GEMINI_API_KEY`: Authentication for Gemini Oracle service
- `LUMO_API_KEY`: Authentication for Lumo AI service  
- `COPILOT_API_KEY`: Authentication for GitHub Copilot service
- `SESSION_SECRET`: Flask session security key (optional, has fallback)