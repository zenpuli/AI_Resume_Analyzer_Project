class AuthService {
  static bool _loggedIn = false;
  static String? _userName;
  static String? _email;

  static bool isLoggedIn() => _loggedIn;
  static String get userName => _userName ?? "User";
  static String get email => _email ?? "";

  static Future<bool> login(String email, String password) async {
    await Future.delayed(const Duration(seconds: 1)); // simulate API
    _loggedIn = true;
    _email = email;
    _userName = email.split('@')[0]; // temporary username
    return true;
  }

  static Future<bool> register(String name, String email, String password) async {
    await Future.delayed(const Duration(seconds: 1)); // simulate API
    return true;
  }

  static void logout() {
    _loggedIn = false;
    _userName = null;
    _email = null;
  }
}
