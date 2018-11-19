The card scanner input involves something called a "serial port", python has a "serial" library that can be used to read this.

python -m serial.tools.list_ports
The above line in terminal will list available ports

If a script throws an "ACCESS DENIED" error, simply close any programs that might be using the port
If that doesn't work, open Task Manager and kill any Python or C# processes that may be holding it open.

newScannerApp.py is currently what i'm using to detect card swipes but I can't send KeyboardInterrupts to break the loop, so I have to kill the program completely with Ctrl+PgUp
The swiper sends a byte-string with many unreadable characters, but the ID is intact. "b';0000000000000180677?\r\n'" is what I get sent, without "" 

Now that the scanner works, I need to start working with google Sheets.

Scanner and Google Sheets integration now works

This is where we purchased the card scanner:
https://www.amazon.com/MagTek-21040108-Magnetic-Keyboard-Emulation/dp/B0009XB10Q

TODO
-Automatically create copies of the sign-in sheet each semester