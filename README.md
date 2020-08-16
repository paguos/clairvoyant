# Clairvoyant

A toolkit for predicting the future using well established time series analysis tools.

## Concept

Try different time series analysis tool with the following workflow:

1. Select a framework (agent) with init parameters
2. Train different parameters to find the right configuration
3. Predict the future

### Agents

An agent integrate a framework into Clairvoyant. 

List of implemented agents:

- **ProphetAgent:** Supports the [Facebook's Prophet](https://facebook.github.io/prophet/) procedure



## Development

Install the dependencies:

```sh
make install
```

Run the tests:

```sh
make tests
```
