<?php
define("TOKEN", "f76c9d689721f5235590f74ae19c6f42");                                       // The secret token to add as a GitHub or GitLab secret, or otherwise as https://www.example.com/?token=secret-token
define("REMOTE_REPOSITORY", "git@github.com:KeydownR/optiroom.git"); // The SSH URL to your repository
define("DIR", "/var/www/optiroom/");                          // The path to your repostiroy; this must begin with a forward slash (/)
define("BRANCH", "refs/heads/dev");                                 // The branch route
define("LOGFILE", "./deploy.log");                                       // The name of the file you want to log to.
define("GIT", "/usr/bin/git");                                         // The path to the git executable
define("AFTER_PULL", "");                                              // A command to execute after successfully pulling
