import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://127.0.0.1:8000";

  static Future<Map<String, dynamic>> analyzeResume(
      List<int> bytes, String filename) async {
    try {
      var request =
          http.MultipartRequest('POST', Uri.parse('$baseUrl/analyze'));

      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          bytes,
          filename: filename,
        ),
      );

      final response = await request.send().timeout(
            const Duration(seconds: 15),
          );

      final responseData = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        return json.decode(responseData);
      } else {
        throw Exception("Server error");
      }
    } catch (e) {
      // fallback when backend is not connected
      return {
        "score": 0,
        "skills": [],
        "missing_skills": [],
        "top_jobs": [],
        "error": "Backend not connected"
      };
    }
  }
}
