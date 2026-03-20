import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "https://ai-resume-analyzer-project-6c8x.onrender.com";

  static Future<Map<String, dynamic>> analyzeResume(List<int> bytes, String filename) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/analyze-resume'));
      request.files.add(http.MultipartFile.fromBytes('file', bytes, filename: filename));

      final response = await request.send().timeout(const Duration(seconds: 30));
      final responseData = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        return json.decode(responseData);
      } else {
        throw Exception("Server Error: ${response.statusCode}");
      }
    } catch (e) {
      print("❌ Connection Error: $e");
      return {"error": "Backend connection failed"};
    }
  }
}