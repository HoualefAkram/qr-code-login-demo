# QR Code TV Login Demo

A simple demonstration of a QR code login flow for TV / device authentication using FastAPI.

This is similar to how many platforms allow users to log in to a TV by scanning a QR code with their phone.

---

## Overview

The flow works as follows:

1. TV generates a UUID
2. The TV sends the UUID to the backend
3. The backend stores it with state `pending`
4. The TV displays a QR code containing a login URL with the UUID
5. The user scans the QR code with their phone
6. The user logs in on the phone
7. The phone sends the authentication token to the backend
8. The TV periodically polls the backend
9. Once the token is available, the TV logs the user in

---

## Architecture

TV Device</br>
    |</br>
    | PUT /login (uuid)</br>
    v</br>
Backend (FastAPI) </br>
    | </br>
    | state = pending </br>
    | </br>
    v </br>
QR Code shown on TV

User Phone </br>
    | </br>
    | Scan QR Code </br>
    v </br>
Website Login </br>
    | </br>
    | PATCH /login (uuid + token) </br>
    v </br>
Backend updates state = accepted

TV Polling </br>
    | </br>
    | GET /login (uuid) </br>
    v </br>
Token returned -> TV logs in

---

## API Endpoints

### Create Login Session

Used by the TV after generating a QR code UUID.

PUT /login

Parameters:

uuid: str

Example response:

{
  "state": "pending",
  "expires_at": "2026-03-09T12:00:00"
}

---

### Complete Login

Used by the mobile device after the user logs in.

PATCH /login

Parameters:

uuid: str  
token: str

This updates the login session to `accepted`.

---

### Poll Login State

Used by the TV to check whether the login is complete.

GET /login

Parameters:

uuid: str

Example responses.

Pending:

{
  "state": "pending",
  "expires_at": "2026-03-09T12:00:00"
}

Accepted:

{
  "state": "accepted",
  "token": "user_auth_token"
}

---

## Expiration

Each login session automatically expires after 5 minutes.

If a session expires, it is removed from the server.

---

## Running the Project

### 1 Install dependencies

pip install fastapi uvicorn

### 2 Start the server

uvicorn main:app --reload

### 3 Open API documentation

http://127.0.0.1:8000/docs

FastAPI automatically provides interactive documentation.

---

## Important Notes

This project is a demo implementation.

For production use you should:

- Store sessions in a database (Redis or PostgreSQL)
- Use secure tokens
- Implement rate limiting
- Use HTTPS
- Ensure UUIDs are cryptographically secure
- Remove tokens after first retrieval

---

## License

MIT