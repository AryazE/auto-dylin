# auto-dylin
Run [DyLin](https://github.com/AryazE/DyLin) inside your GitHub workflow.
DyLin is a dynamic linter that checks the execution of your code for common mistakes and anti-patterns.

## Usage
 DyLin first instruments the code based on the selected checkers, and then after the execution, generates a report of its findings.  
 A typical GitHub workflow has the following structure:
 ```yaml
    <Check out the repository>
    <Install the requirements>
    <Run tests>
    <Clean up ad generate reports>
 ```
 You need to insert the instrumentation action right before running the code, and the action to generate the report right after the code is executed as below:
 ```yaml
    <Check out the repository>
    <Install the requirements>
    - name: Instrument code
      uses: AryazE/auto-dylin/instrument@main
    <Run tests>
    - name: Report findings
      if: always()
      uses: AryazE/auto-dylin/report@main
    <Clean up ad generate reports>
 ```
This will generate a report which will be visible as a summary of the workflow run, and also as an artifact to download.

## Options
The instrument action provides the following options:
```yaml
  path:
    description: 'Path to instrument'
    default: '.'
  include-checkers:
    description: 'Checkers to run'
    default: 'All'  # can be a space-separated string 
                    # of checker codes like
                    # `'ML-01 ML-02 ML-03'`
  exclude-checkers:
    description: 'Checkers that will not run'
    default: 'None' # can be a space-separated string 
                    # of checker codes like
                    # `'ML-01 ML-02 ML-03'`
  analysis-coverage:
    description: 'Whether to collect analysis coverage'
    default: true   # can be `false`
```
