# AV-Competition-Software

Repository for the autonomous vehicle building competition.

Participants should write their code in the behavior.py file, within the provided function, while the vehicle should be run with the run.py script.

MCAV provided code should be contained within the mcav_av_workshop package, as well as some structure within run.py.

## Useful & troubleshooting commands

```bash
sudo chmod 666 /var/run/docker.sock 
```

## Setting up Pi's
- Ensure users are added to the docker usergroup, so that they can run `inference server start`
```bash
# Check whether $USER is defined
echo $USER

# Add user to docker group
sudo usermod -aG docker $USER
```
