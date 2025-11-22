## Solo clic en pagar (usando Chrome ya abierto)
1. Abre Chrome con depuración:  
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-bot-1"`  
   Ve a `https://www.flexispot.es/checkout` y rellena todo a mano.
2. Lanza el clic programado:  
   `python click_only.py --debugger-address 127.0.0.1:9222 --run-at 2025-11-28T00:00:00`
   - Si no quieres programar hora, omite `--run-at` y clicará en cuanto el botón esté clickable.
   - `--timeout` ajusta la espera para localizar el botón (default 20s).

### Varias ventanas a la vez
- Arranca varias instancias de Chrome con puertos y perfiles distintos, ej.:  
  - `--remote-debugging-port=9222 --user-data-dir="/tmp/chrome-bot-1"`  
  - `--remote-debugging-port=9223 --user-data-dir="/tmp/chrome-bot-2"`  
  - `--remote-debugging-port=9224 --user-data-dir="/tmp/chrome-bot-3"`
- En cada una, abre checkout y rellena.
- Ejecuta un `click_only.py` por cada puerto:  
  `python click_only.py --debugger-address 127.0.0.1:9222 --run-at ... &`  
  `python click_only.py --debugger-address 127.0.0.1:9223 --run-at ... &`  
  `python click_only.py --debugger-address 127.0.0.1:9224 --run-at ... &`
