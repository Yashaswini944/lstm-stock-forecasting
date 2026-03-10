# LSTM Forecasting API – Manual Test Cases

| ID         | Feature        | Scenario                                      | Steps                                                                 | Expected Result                                      |
|------------|----------------|-----------------------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------|
| TC_LSTM_01 | API            | Valid forecast request                        | 1. POST /predict with valid JSON series                               | 200 OK + predictions array                          |
| TC_LSTM_02 | Validation     | Missing required field                        | 1. POST /predict with empty JSON                                      | 400 Bad Request + validation error                  |
| TC_LSTM_03 | Validation     | Wrong data type                               | 1. POST /predict with strings instead of numbers                      | 400 Bad Request                                     |
| TC_LSTM_04 | Boundary       | Very short time series                        | 1. POST minimal allowed data                                          | Clear error or valid prediction                     |
| TC_LSTM_05 | Boundary       | Very long time series                         | 1. POST large dataset                                                 | No crash, reasonable response time                  |
| TC_LSTM_06 | Error Handling | Internal model error                          | 1. Break model path 2. POST /predict                                  | 500 with safe error message                         |
| TC_LSTM_07 | Regression     | Re-test after model update                    | 1. Update model 2. Repeat TC_LSTM_01                                  | Endpoint still works                                |
| TC_LSTM_08 | Negative       | Empty payload                                 | 1. POST /predict with no body                                         | 400 Bad Request                                     |
| TC_LSTM_09 | Performance    | Response time                                 | 1. POST valid request 2. Measure time                                 | < 2 seconds                                         |
| TC_LSTM_10 | API Contract   | Check response structure                      | 1. POST valid request 2. Inspect JSON                                 | Contains expected keys                              |
