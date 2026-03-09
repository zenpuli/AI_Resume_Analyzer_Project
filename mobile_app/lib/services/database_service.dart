import 'package:cloud_firestore/cloud_firestore.dart';
import 'auth_service.dart';

class DatabaseService {
  static final FirebaseFirestore _db = FirebaseFirestore.instance;

  /// Saves the complete analysis history under the user's secure UID
  static Future<void> saveAnalysisResult(Map<String, dynamic> results) async {
    final String userId = AuthService.uid;

    // Safety check for Guest users
    if (userId.isEmpty || userId == "") return;

    try {
      // Extract specific fields for quick queries while saving raw_data for UI detail
      await _db.collection('users').doc(userId).collection('history').add({
        'timestamp': FieldValue.serverTimestamp(),
        'overall_score': results['scores']?['overall'] ?? 0,
        'predicted_role': (results['top_3_roles'] != null && results['top_3_roles'].isNotEmpty)
            ? results['top_3_roles'][0]['role']
            : "Unknown",
        'raw_data': results, // Dynamic model output for reloading the AnalysisScreen
      });
      print("✅ [FIRESTORE] Resume Analysis Archive Created.");
    } catch (e) {
      print("❌ [FIRESTORE ERROR] Could not save history: $e");
    }
  }
}