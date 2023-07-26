Feature: Security checks
  In order to check the security features of P-KISS-SBC
  I want to block unwanted calls and perform assertions on their progress

  Scenario: R-URI user part is not phone number
    Given the following providers exist in the address table of the database:
      | grp | ip_addr   | mask | port | tag |
      | 2   | 10.0.3.10 | 32   | 5060 | 200 |
    Given the following IPBXs exist in the address table of the database:
      | grp | ip_addr  | mask | port | tag |
      | 1   | 10.0.3.2 | 32   | 5060 | 100 |
    And the following rules exist in the dialplan table of database:
      | dpid | pr | match_op | match_exp          | match_len | subst_exp | repl_exp | attrs |
      | 2    | 1  | 1        | ^\\+33[1-9][0-9]+$ | 12        | 1         | 1        | 201   |
      | 2    | 1  | 1        | ^0[1-9][0-9]+$     | 10        | 1         | 1        | 200   |
    And the following destinations exist in the dispatcher table of database:
      | setid | destination    | flags | priority | attrs            | description |
      | 200   | 10.0.3.10:5060 | 0     | 0        | sockname=public  | prov1       |
      | 201   | 10.0.3.20.5060 | 0     | 0        | sockname=public  | prov2       |
    When SBC receives an SIP INVITE from this source "<ip>"/"<port>" with one of this "<number>" in R-URI userpart
    Then SBC generates a response to provider with this "<code>" and "<message>"

  Examples:
    | ip        | port | did          | code | message                    |
    | 10.0.3.10 | 5060 | a34240506070 | 404  | Dialed number is not valid |
    | 10.0.3.2  | 5060 | a34240506070 | 404  | Dialed number is not valid |