import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'dart:async';

class AuthService {
  static final FirebaseAuth _auth = FirebaseAuth.instance;
  static final FirebaseFirestore _db = FirebaseFirestore.instance;

  static String get email => _auth.currentUser?.email ?? "Guest";
  static String get uid => _auth.currentUser?.uid ?? "";
  static String userName = "User";

  static bool isLoggedIn() => _auth.currentUser != null;

  /// ⚡ INSTANT LOGIN: Returns "success" before fetching profile data
  static Future<String?> login(String email, String password) async {
    if (!email.toLowerCase().endsWith('@gmail.com')) return "invalid_format";

    try {
      UserCredential userCredential = await _auth
          .signInWithEmailAndPassword(email: email, password: password)
          .timeout(const Duration(seconds: 5));

      // ⚡ ASYNC FETCH: Don't 'await' this. Navigate first, load name in background.
      _db.collection('users').doc(userCredential.user!.uid).get().then((doc) {
        if (doc.exists) userName = doc.data()?['name'] ?? "User";
      });

      return "success";
    } on FirebaseAuthException catch (e) {
      if (e.code == 'user-not-found' || e.code == 'invalid-credential') return "no_user";
      if (e.code == 'wrong-password') return "wrong_password";
      return "low_signal";
    } catch (e) {
      return "low_signal";
    }
  }

  /// ⚡ FAST REGISTER: Creates account and background-saves profile
  static Future<String?> register(String name, String email, String password) async {
    if (!email.toLowerCase().endsWith('@gmail.com')) return "invalid_format";

    try {
      UserCredential res = await _auth.createUserWithEmailAndPassword(email: email, password: password);
      
      // ⚡ ASYNC WRITE: Fire and forget the profile creation to speed up UI
      _db.collection('users').doc(res.user!.uid).set({
        'name': name,
        'email': email,
        'createdAt': FieldValue.serverTimestamp(),
      });
      
      userName = name;
      return "account_created";
    } on FirebaseAuthException catch (e) {
      if (e.code == 'email-already-in-use') return "user_exists";
      return "error";
    }
  }

  static Future<void> logout() async => await _auth.signOut();
}