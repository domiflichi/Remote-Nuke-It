//
// Note - this script is very rough and crude. There could be many improvements made to it
// 



// Codes from NodeJS server:
// 
// 000 = 'Nojoy' / Nothing to do
// 111 = Web server could not find corresponding file (Log this on client side!)
// 222 = Execute / Nuke!
// 

 

const http = require("http");
let url = require('url');


let fileExistsFlag = false;
let fileWriteFlag = false;
let fileResetFlag = false;

const host = '192.168.1.10';                // ********** Change this value to meet your needs ************
const port = 8003;                          // ********** Change this value to meet your needs ************

const fs = require('fs');                   // Using this to check if the file exists




const requestListener = function (req, res) {
    //res.writeHead(200, {'Content-Type': 'text/plain', 'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': 0});
    res.writeHead(200, {'Content-Type': 'text/plain'});     // Write header to browser
    var q = url.parse(req.url, true).query;                 // Set up a variable, q, to parse the URL


    try {                                                   // Let's check if the file (corresponding to the CID in the querystring) exists
        if (fs.existsSync(q.CID + '.txt')) {
                                                            // Yes, file exists!
            console.log('File Exits!!!!');                  // Write out to the console that the file does not exist
            fileExistsFlag = true;                          // Set our flag to true
    
        } else {
            //res.write('No file found!\n');
            res.end('111');                                 // Write out '111' to browser - which, in this little app, represents that the file in the querystring does not exist
            console.log('File does NOT exist :(');          // Write out to the console that the file does not exist
            fileExistsFlag = false;                         // Set our flag to false
        }
        } catch(err) {                                      // Catch an error
            console.error(err);                             // And write out to console
        }


      if (fileExistsFlag) {                                         // If the file exists

        fs.readFile(q.CID + '.txt', 'utf8', (err, data) => {        // Read the file
            if (err) {                                              // If there was an error
              console.error(err);                                   // Write out the error to the console
              return;
            }

            //       *****************      Note - it seems that working with the 'data' variable has some severe limitations:
            //       *****************             The value of it can not be written to the browser unless it is used at the end - res.end
            //       *****************           As opposed to the beginning/middle, using res.write!!!
            //       *****************             I even tried creating a separate variable and assigning it the value, to refer to it later, but
            //       *****************             but that did not work either. :(
            //       *****************           I do acknowledge however that it could be something that I'm doing wrong - maybe there IS a way to use it
            //       *****************             without it being at the end, but I don't really *need* to at the moment, so I'll live with it for now
            //       *****************
            //       *****************      Update - I had problems with res.write in other parts of the code too - I just can't seem to get it to work in some places



            // Look at the querystring name/value pair called 'requestreason'
            if (q.requestreason=='execute') {                                                   // If the value is 'execute' - we need to update the appropriate .txt file to say (only): 222 (execute)

                console.log('Updating contents of ' + q.CID + '.txt to 222 (execute)!');        // Write message to console showing we're writing new content

                const fsw = require('fs');                                                      // New constant for file writing
                const newfilecontent = '222';                                                   // New constant to hold the new, file content we are about to write

                fsw.writeFile(q.CID + '.txt', newfilecontent, err => {                          // Write the new content to our file
                    if (err) {                                                                  // If there's an error
                        console.error(err);                                                     // Write out the error to the console
                    } else {
                        // file written successfully
                        fileWriteFlag = true;                                                   // Update our fileWriteFlag flag to true if successful (which is just a 'dummy' thing to do - we don't actually use this anywhere else)
                    }
                });

            } else if (q.requestreason=='checkin') {                                            // If the value of 'requestreason' is 'checkin', then...
                console.log('Just checking in - not taking any action');                        // Write out to the console that it's just a checkin
                fileResetFlag = true;                                                           // Set this flag to true...we may need to use it later...
            } else {
                console.log('Unrecognized value - ignoring');                                   // If requestreason = anything else, we're just going to ignore it, so write that out to the console
            }


            // If the requestreason is 'checkin' and the file contains '222' (execute), we can assume that this is the Python script just checking in
            //   to see if it needs to delete data (execute). This means that we want to reset the file back to '000' (nojoy) also so that the Python
            //   script won't keep trying to 'execute' after it already has.
            if (fileResetFlag && data=='222') {                                                 // If fileResetFlag is true and 'data' = '222', then...

                console.log('We need a reset!');                                                // Write out to our console that we need a reset

                const fswresetfile = require('fs');                                             // Set up a constant to write to the file system
                const newfilecontent = '000';                                                   // Set up a constant for the new contents of the file

                fswresetfile.writeFile(q.CID + '.txt', newfilecontent, err => {                 // Attempt to write the new contents of the file
                    if (err) {                                                                  // If there's an error though,
                        console.error(err);                                                     // Write out the error to the console
                    } else {                                                                    // Otherwise,
                        console.log('File contents updated to 222');                            // Write out to the console that we successfully updated the contents of the file to '222'
                    }
                });

                fileResetFlag = false;                                                          // Reset this flag back to false
            }


            res.end(data);                                                                      // write contents of file to browser (should just be 1 line)
            console.log(data);                                                                  // write contents of file to console

          });

      }


};



const server = http.createServer(requestListener);                  // Set up a constant for our server

server.listen(port, host, () => {                                   // Start our web server on specified 'host' and 'port'
    console.log(`Server is running on http://${host}:${port}`);     // Write out to our console what 'host' and 'port' our server is running on
});

