<img width="1320" height="966" alt="image" src="https://github.com/user-attachments/assets/39a01122-e15a-46e9-be09-394b755599ae" />



🏥 Multi-Role Firebase Flutter App

This project demonstrates a role-based access system using Flask + Firebase + Flutter:

Roles: Doctor, Patient, Counselor

Users are created via a Flask admin dashboard

Flutter app shows role-specific screens



🔐 Firestore Security Rules

Paste the following in Firebase Console → Firestore → Rules:

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      // A user can only read their own document
      allow read: if request.auth != null && request.auth.uid == userId;
      // Only Flask backend can write
      allow write: if false;
    }
  }
}

✅ Only the Flask server can create users.
✅ Users can only read their own data.

⚙️ Workflow
Admin opens Flask dashboard
       ↓
Fills name / email / password / role → clicks "Create Account"
       ↓
Flask creates Firebase Auth user + writes role to Firestore
       ↓
User opens Flutter app → enters email & password
       ↓
Firebase Auth validates credentials
       ↓
Flutter fetches role from Firestore
       ↓
Doctor → Blue screen
Patient → Green screen
Counselor → Purple screen
