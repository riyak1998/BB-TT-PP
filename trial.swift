import Foundation
import CoreServices.DictionaryServices
func isWord(input:String)-> Int{
    let t = input.components(separatedBy: " ");
    var count=0.0;
    let cutoff = 0.7 * Double(t.count)
    for ele in t{
        let nsstring = ele as NSString;
        let cfrange = CFRange(location: 0, length: nsstring.length);
        let ans = DCSCopyTextDefinition(nil,nsstring,cfrange);
        if !(ans==nil) {
            count = count+1;
        }
        if(count>=cutoff){
            return 1;
        }
    }
    return 0;  
}
print(isWord(input : CommandLine.arguments[1]));
