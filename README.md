# Orwell for AWS Workspaces


# orwell4awsws
![alt text](https://www.peaceproject.com/wp-content/uploads/LS255-In-Time-Of-Universal-Deceit-Bumper-Sticker.jpg?sfvrsn=74f89f35_1 "Orwell for AWS Workspaces")


## Summary
Tooling to gather utilization data from AWS Workspaces via API, aggregate with pandas and numpy and publish pivot reports showing user online and offline time in a variety of views.

# Getting Started

## Prerequsites
_Note: The way I like things, plenty of other options._
- Minicond Python distro (https://docs.conda.io/en/latest/miniconda.html)
- Nginx for publishing reports
-- This is not an Nginx tutorial, but I suggest using fancy indexing which will likely require installing "nginx-extras".

## Optional
- If you want to stream live data you will streaming you will need an Initalstate account (https://www.initialstate.com/)
_Note: Again lots of option here, I am only providing the option I utilzed._

![alt text](https://imgur.com/a/0hq6nz7 "orwell4awsws streaming dashboard")

## Installation 
- Download code from GitHub
```
git clone https://github.com/rbocchinfuso/orwell4awsws.git
```
_Note:  If you don't have Git installed you can also just grab the zip: https://github.com/rbocchinfuso/orwell4awsws/archive/master.zip_

- Make sure the orwell4awsws dir and files have proper ownership and permissions
- Install miniconda
- Create env
`conda create env`
- Activate env
`conda activate env`
- Install requirements
`pip install -r requirements.txt`
- Copy config.ini.example to config.ini
- Modify settings in config.ini
_Note: Initialstate information only required if you want to use the ISStreamer to stream realtime connection data for connection visualization._
- Configure the AWS CLI
-- Not an AWS tutorial but you will need an IAM role with the appropriate access and 

# Usage

## Run
`nohup python orwell4awsws.py >/dev/null 2>&1 &`

## Report generation cron job
`0 * * * * python [PATH]/orwell4awsws/orwellpivot.py > [PATH]orwell4awsws/orwellpivot.log 2>&1`


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request ツ

## History
-  version 0.1.0 (initial release) - 2020/03/19

## Credits
Rich Bocchinfuso <<rbocchinfuso@gmail.com>>


## License
MIT License

Copyright (c) [2020] [Richard J. Bocchinfuso]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.