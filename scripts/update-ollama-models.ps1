ollama list | Select-Object -Skip 1 |
  ForEach-Object { ($_.ToString().Trim() -split '\s+')[0] } |
  ForEach-Object { ollama pull $_ }
