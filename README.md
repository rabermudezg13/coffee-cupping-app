# ☕ Coffee Cupping App

A streamlined coffee cupping application built with Python and Streamlit, featuring persistent user accounts, preferences management, and responsive design.

## Features

### 🔐 User Management
- **Registration**: Create account with email, username, and password
- **Login**: Sign in with email or username
- **Persistence**: User accounts persist across sessions and redeployments
- **Validation**: Email format, username rules, and password strength validation

### ⚙️ User Preferences
- **Display Name**: Choose to show username or post as "Anonymous"
- **Email Notifications**: Toggle email notifications on/off
- **Theme Selection**: Light/dark theme preferences
- **Database Persistence**: All preferences saved to Firestore

### 🎨 Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Desktop Support**: Full desktop experience
- **Coffee Theme**: Beautiful coffee-inspired color scheme
- **Modern UI**: Clean, card-based interface with smooth animations

## Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with Firebase Admin SDK
- **Database**: Google Firestore (NoSQL)
- **Authentication**: Custom auth with bcrypt password hashing
- **Deployment**: Ready for Streamlit Cloud or any Python hosting

## Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd coffeeApp
pip install -r requirements.txt
```

### 2. Firebase Setup
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project
3. Enable Firestore Database
4. Go to Project Settings → Service Accounts
5. Generate new private key (downloads JSON file)
6. Copy `.env.example` to `.env` and fill in your credentials:

```env
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com
```

### 3. Run the App
```bash
streamlit run app.py
```

## Database Schema

### Users Collection (`users`)
```json
{
  "user_id": "unique_uuid_string",
  "email": "user@example.com",
  "username": "coffeeexpert",
  "password_hash": "bcrypt_hashed_password",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z",
  "preferences": {
    "show_name": true,
    "email_notifications": true,
    "theme": "light"
  }
}
```

### Field Descriptions
- **user_id**: Unique identifier (UUID4)
- **email**: User's email address (unique)
- **username**: Display username (unique, 3-20 chars)
- **password_hash**: Bcrypt hashed password
- **created_at**: Account creation timestamp
- **last_login**: Last login timestamp
- **preferences.show_name**: `true` shows username, `false` shows "Anonymous"
- **preferences.email_notifications**: Email notification preference
- **preferences.theme**: UI theme preference

## Project Structure

```
coffeeApp/
├── app.py              # Main Streamlit application
├── auth.py             # Authentication manager
├── database.py         # Firestore database operations
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env               # Your environment variables (create this)
└── README.md          # This file
```

## Features in Detail

### Registration
- Email validation (proper email format)
- Username validation (3-20 characters, alphanumeric + underscore)
- Password strength (minimum 6 characters)
- Duplicate check (email and username must be unique)
- Secure password hashing with bcrypt

### Login
- Support for both email and username login
- Password verification against hash
- Session state management
- Last login timestamp tracking
- Persistent login across page refreshes

### User Preferences
- **Display Name Control**: Users can choose to show their username or post as "Anonymous"
- **Email Notifications**: Toggle for future email features
- **Theme Selection**: Light/dark mode preference
- **Real-time Updates**: Changes reflect immediately in the UI
- **Database Persistence**: All preferences saved to Firestore

### Security Features
- Bcrypt password hashing (industry standard)
- Input validation and sanitization
- Session-based authentication
- No passwords stored in plain text
- Secure environment variable handling

### Responsive Design
- Mobile-optimized layout
- Responsive columns that stack on mobile
- Touch-friendly buttons and forms
- Coffee-themed color scheme
- Smooth animations and transitions

## Usage

### For Users
1. **Register**: Create account with email, username, and password
2. **Login**: Sign in with your credentials
3. **Customize**: Update preferences in Settings tab
4. **Logout**: Securely log out when done

### For Developers
The app is designed for easy extension:

#### Adding New User Fields
```python
# In database.py, modify create_user method
user_data = {
    'user_id': user_id,
    'email': email,
    'username': username,
    'password_hash': password_hash,
    'your_new_field': value,  # Add here
    # ... rest of fields
}
```

#### Adding New Preferences
```python
# In auth.py, update default preferences
'preferences': {
    'show_name': True,
    'email_notifications': True,
    'theme': 'light',
    'your_new_preference': default_value  # Add here
}
```

#### Customizing UI
The CSS is in `app.py` within the `st.markdown()` call. Modify the CSS variables:
```css
:root {
    --coffee-brown: #8B4513;
    --coffee-light: #D2B48C;
    --coffee-cream: #F5DEB3;
}
```

## Deployment

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Add environment variables in Streamlit Cloud settings
4. Deploy!

### Other Platforms
The app works on any platform that supports Python and Streamlit:
- Heroku
- Railway
- Render
- Google Cloud Run
- AWS ECS

### Environment Variables for Deployment
Make sure to set these environment variables in your deployment platform:
- `FIREBASE_TYPE`
- `FIREBASE_PROJECT_ID`
- `FIREBASE_PRIVATE_KEY_ID`
- `FIREBASE_PRIVATE_KEY`
- `FIREBASE_CLIENT_EMAIL`
- `FIREBASE_CLIENT_ID`
- `FIREBASE_AUTH_URI`
- `FIREBASE_TOKEN_URI`
- `FIREBASE_AUTH_PROVIDER_X509_CERT_URL`
- `FIREBASE_CLIENT_X509_CERT_URL`

## Testing Persistence

To verify that user accounts persist:

1. **Register** a new account
2. **Close** the browser tab
3. **Reopen** the app
4. **Login** with your credentials
5. **Verify** your preferences are maintained

The account should persist even after:
- Page refresh
- Browser restart
- App redeployment
- Server restart

## Troubleshooting

### Firebase Connection Issues
- Verify Firebase project ID is correct
- Check that Firestore is enabled
- Ensure service account has proper permissions
- Validate private key format (with \n for line breaks)

### Login/Registration Problems
- Check Firebase rules allow read/write
- Verify internet connection
- Clear browser cache if issues persist
- Check browser console for JavaScript errors

### Mobile Display Issues
- Clear browser cache
- Try in incognito/private mode
- Check CSS media queries are loading

## Future Enhancements

This foundation is ready for:
- Coffee cupping form and data
- Social features and sharing
- Analytics and reporting
- Photo upload capabilities
- Email notifications
- Admin panel
- API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

---

Built with ☕ and ❤️ using Streamlit and Firebase