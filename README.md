# Sensu metrics per process
This scrip will help you to collect metrics based on per process. Required process name as a argument, also able to kill that process if desired thresould crossed.



## Getting Started

pull the script and place it under sensu embedded directory.

```/opt/sensu/embedded/bin/metrics_per_process.py```


now create a config for the check /etc/sensu/conf.d/myapp.json
```
{
  "checks": {
  "myapp-stats": {
     "type": "metric",
     "command":"/opt/sensu/embedded/bin/metrics_per_process.py -p /home/user/my-app.js",
     "interval": 60,
     "subscribers": [
       "my-app"
     ],
    "handler": "librato"
  }
 }
```

### Prerequisites

psutil

`pip install psutil`
```

```


## Contributing

Please read [CONTRIBUTING.md](https://github.com/Adiii717/sensu_installtion/blob/master/Good-CONTRIBUTING.md-template.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Adil Mehmood DevOps Engineer** - *Initial work* - [ThinkDifferent](https://github.com/Adiii717)

See also the list of [contributors](https://github.com/Adiii717/sensu-per-process-metrics/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments



