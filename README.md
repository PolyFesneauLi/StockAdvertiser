# StockAdvertiser

## how to start up
### for cmd in windows
start /B cmd /c "python -m http.server 8000" & start http://localhost:8000
### for powershell in windows 
Start-Process cmd -ArgumentList '/c python -m http.server 8000' -WindowStyle Hidden; Start-Process http://localhost:8000
### for macOS
nohup python -m http.server 8000 & open http://localhost:8000
