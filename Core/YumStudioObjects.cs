using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

/// YumStudioObject
/// 
/// Custom Object Notation Format, provided by YumStudio.
/// This is free and open-source, but please, credit us (At YumStudio, https://github.com/YumStudioHQ).
/// This code is provided "as is", so you're resonsible of everything can happen by it.
/// Thank you using our format!
/// 
/// Author: Wys (https://github.com/wys-prog)

namespace YumStudio;

public class YSObject
{
  /// <summary>
  /// Each object must belong to a scope.
  /// We can represent scopes by using Dictionary<string, string>.
  /// But each objects can contain multiple scopes, allowing for example redefinition of some symbols
  /// in different scopes. So to represent scopes (which are labeled by a string too), we'll use a 
  /// Dictionary<string, Dictionary<string, string>>, where the nesteded dictionary is all our
  /// symbols and their values, while the string used as key is simply the name of the scope.
  /// Note: Names are UTF-8, and can be any character supported by System.String (even numbers)
  /// </summary>
  public Dictionary<string, Dictionary<string, string>> Keys = [];

  public void AddKeys(Dictionary<string, Dictionary<string, string>> @keys)
  {
    
  }

  public YSObject() { } // Does nothing! (fr)
}

public class YSObjectParser
{
  private readonly Dictionary<string, Dictionary<string, string>> Keys = [];
  private string currentLabel = "";

  public void ParsePart(string part)
  {
    part = part.Trim();
    if (part.StartsWith(';')) return;
    else if (part.StartsWith('['))
    {
      var beg = part.IndexOf('[');
      var end = part.IndexOf(']');
      if (end == -1) throw new FormatException("expected ']' when '[' is present");
      currentLabel = part[(beg + 1)..end];
      if (!Keys.ContainsKey(currentLabel)) Keys[currentLabel] = [];
    }
    else
    {
      if (part.Contains(':'))
      {
        var parts = part.Split(':', 2, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        if (parts.Length < 2) throw new FormatException();

        Keys[currentLabel][parts[0]] = parts[1];
      } // Else, it's an orphelan data.
    }
  }

  public YSObject FromFile(string path)
  {
    var obj = new YSObject();

    using StreamReader reader = new(path);
    while (!reader.EndOfStream)
    {
      var line = reader.ReadLine();
      ParsePart(Regex.Unescape(line.Trim()));
    }

    obj.Keys = Keys;

    return obj;
  }

  public YSObject FromString(string s)
  {
    var obj = new YSObject();

    var parts = s.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
    foreach (var part in parts)
    {
      ParsePart(Regex.Unescape(part));
    }

    obj.Keys = Keys;

    return obj;
  }

  public static YSObject Parse(string source, bool isFile = true)
  {
    YSObjectParser obj = new();
    return isFile ? obj.FromFile(source) : obj.FromString(source);
  }
}