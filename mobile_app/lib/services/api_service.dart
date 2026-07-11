import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // ✅ Base URL cleanly structured with trailing slash
  static const String baseUrl = "https://ai-resume-analyzer-project-6c8x.onrender.com/";

  static Future<Map<String, dynamic>> analyzeResume(List<int> bytes, String filename) async {
    try {
      // Combines to perfect endpoint path string mapping
      final targetUri = Uri.parse('${baseUrl}analyze-resume');
      print("🚀 [NETWORK CALL] Post payload streaming to: $targetUri");
      
      var request = http.MultipartRequest('POST', targetUri);
      
      // Inject bytes directly into multi-part form parameters matching FastAPI context schema
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          bytes,
          filename: filename,
        ),
      );

      // Free tier cold starts can take a moment; 60 seconds gives it high structural stability
      final streamedResponse = await request.send().timeout(const Duration(seconds: 60));
      final responseData = await http.Response.fromStream(streamedResponse);

      print("📊 [NETWORK RESPONSE] Server returned status code: ${responseData.statusCode}");

      if (responseData.statusCode == 200) {
        final decodedData = json.decode(responseData.body);
        return decodedData;
      } else {
        print("🚨 Backend Error payload: ${responseData.body}");
        return {"error": "Server returned status error: ${responseData.statusCode}"};
      }
    } catch (e) {
      print("❌ Connection Exception encountered: $e");
      return {"error": "Backend connection failed"};
    }
  }
}