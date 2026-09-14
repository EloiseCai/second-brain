import Foundation
import Vision
import AppKit

let root = URL(fileURLWithPath: ".content_collect_batch4")
let input = root.appendingPathComponent("items.json")
let data = try Data(contentsOf: input)
var json = try JSONSerialization.jsonObject(with: data) as! [String: Any]
var items = json["items"] as! [[String: Any]]

func recognize(_ path: String) -> String {
    guard let image = NSImage(contentsOfFile: path),
          let tiff = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let cg = bitmap.cgImage else { return "" }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    request.recognitionLanguages = ["zh-Hans", "en-US"]
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([request])
        return (request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
    } catch { return "" }
}

for i in items.indices {
    guard var images = items[i]["images"] as? [[String: Any]] else { continue }
    for j in images.indices {
        if let path = images[j]["localPath"] as? String { images[j]["ocr"] = recognize(path) }
    }
    items[i]["images"] = images
    print("OCR \(i + 1)/\(items.count) \(items[i]["noteId"] ?? "")")
}
json["items"] = items
let output = try JSONSerialization.data(withJSONObject: json, options: [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes])
try output.write(to: input)
