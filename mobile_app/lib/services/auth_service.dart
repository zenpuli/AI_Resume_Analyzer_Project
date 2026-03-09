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

  /// ⚡ ULTRA FAST LOGIN: Background name fetching
  static Future<String?> login(String email, String password) async {
    if (!email.toLowerCase().endsWith('@gmail.com')) return "invalid_format";

    try {
      UserCredential userCredential = await _auth
          .signInWithEmailAndPassword(email: email, password: password)
          .timeout(const Duration(seconds: 6));

      // ⚡ FETCH NAME IN BACKGROUND: Don't 'await' this.
      _db.collection('users').doc(userCredential.user!.uid).get().then((doc) {
        if (doc.exists) userName = doc.data()?['name'] ?? "User";
      });

      return "success";
    } on FirebaseAuthException catch (e) {
      if (e.code == 'user-not-found' || e.code == 'invalid-credential') return "no_user";
      if (e.code == 'wrong-password') return "wrong_password";
      if (e.code == 'network-request-failed') return "low_signal";
      return "error";
    } on TimeoutException {
      return "low_signal";
    } catch (e) {
      return "error";
    }
  }

  /// 🛡️ SECURE REGISTER: Checks if user exists
  static Future<String?> register(String name, String email, String password) async {
    if (!email.toLowerCase().endsWith('@gmail.com')) return "invalid_format";

    try {
      UserCredential res = await _auth.createUserWithEmailAndPassword(email: email, password: password);
      
      await _db.collection('users').doc(res.user!.uid).set({
        'name': name,
        'email': email,
        'createdAt': FieldValue.serverTimestamp(),
      });
      
      userName = name;
      return "account_created";
    } on FirebaseAuthException catch (e) {
      if (e.code == 'email-already-in-use') return "user_exists";
      if (e.code == 'network-request-failed') return "low_signal";
      return "error";
    } catch (e) {
      return "error";
    }
  }

  static Future<void> logout() async => await _auth.signOut();
}