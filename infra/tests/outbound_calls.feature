Feature: Outbound calls
  In order to check the most basic operation of P-KISS-SBC
  I want to be able to process outbound calls and perform assertions on their progress

  Scenario: succesfull routing
    Given the following providers exist in the address table of the database:
      | grp | ip_addr   | mask | port | tag |
      | 2   | 10.0.3.10 | 32   | 5060 | 200 |
      | 2   | 10.0.3.20 | 32   | 5060 | 201 |
    Given the following IPBXs exist in the address table of the database:
      | grp | ip_addr  | mask | port | tag |
      | 1   | 10.0.3.2 | 32   | 5060 | 100 |
      | 1   | 10.0.3.3 | 32   | 5060 | X |
    Given the following X-Tenant SIP header exist in the XXXX table of the database:
      | X-Tenant | tag |
      | ipbx1    | 110 |
      | ipbx2    | 111 |
    And the following rules exist in the dialplan table of database:
      | dpid | pr | match_op | match_exp          | match_len | subst_exp | repl_exp | attrs |
      | 2    | 1  | 1        | ^\\+33[1-9][0-9]+$ | 12        | 1         | 1        | 201   |
      | 2    | 1  | 1        | ^0[1-9][0-9]+$     | 10        | 1         | 1        | 200   |
    And the following destinations exist in the dispatcher table of database:
      | setid | destination    | flags | priority | attrs            | description |
      | 200   | 10.0.3.10:5060 | 0     | 0        | sockname=public  | prov1       |
      | 201   | 10.0.3.20.5060 | 0     | 0        | sockname=public  | prov2       |
    When SBC receives an SIP INVITE from this source "<ip>"/"<port>" with one of this "<number>" in R-URI userpart. The INVITE could contains the "X-Tenant" SIP Header with this value "<tenant>"
    Then SBC generates a new SIP INVITE to gateway with this "<cidr>"

  Examples:
    | ip       | port | tenant | number       | cidr           |
    | 10.0.3.2 | 5060 |        | 0240506070   | 10.0.3.10:5060 |
    | 10.0.3.3 | 5060 | ipbx1  | +33140506071 | 10.0.3.20:5060 |
    | 10.0.3.3 | 5060 | ipbx2  | +33140506072 | 10.0.3.20:5060 |

  Scenario: unkown customer - monotenant and multi tenant
    Given the following providers exist in the address table of the database:
      | grp | ip_addr   | mask | port | tag |
      | 2   | 10.0.3.10 | 32   | 5060 | 200 |
      | 2   | 10.0.3.20 | 32   | 5060 | 201 |
    Given the following IPBXs exist in the address table of the database:
      | grp | ip_addr  | mask | port | tag |
      | 1   | 10.0.3.2 | 32   | 5060 | 100 |
      | 1   | 10.0.3.3 | 32   | 5060 | X |
    Given the following X-Tenant SIP header exist in the XXXX table of the database:
      | X-Tenant | tag |
      | ipbx1    | 110 |
      | ipbx2    | 111 |
    And the following rules exist in the dialplan table of database:
      | dpid | pr | match_op | match_exp          | match_len | subst_exp | repl_exp | attrs |
      | 2    | 1  | 1        | ^\\+33[1-9][0-9]+$ | 12        | 1         | 1        | 201   |
      | 2    | 1  | 1        | ^0[1-9][0-9]+$     | 10        | 1         | 1        | 200   |
    And the following destinations exist in the dispatcher table of database:
      | setid | destination    | flags | priority | attrs            | description |
      | 200   | 10.0.3.10:5060 | 0     | 0        | sockname=public  | prov1       |
      | 201   | 10.0.3.20.5060 | 0     | 0        | sockname=public  | prov2       |
    When SBC receives an SIP INVITE from this source "<ip>"/"<port>" with one of this "<number>" in R-URI userpart. The INVITE could contains the "X-Tenant" SIP Header with this value "<tenant>"
    Then SBC generates a response to provider with this "<code>"

  Examples:
    | ip        | port | tenant | number       | code |
    | 10.0.3.4  | 5060 | ipbx1  | 34240506070  | 403  |
    | 10.0.3.4  | 5060 |        | 34240506070  | 403  |
    | 10.0.3.3  | 5060 | ipbx3  | +34140506071 | 403  |
    | 10.0.3.3  | 5061 |        | +34140506071 | 403  |
    | 10.0.3.3  | 5060 |        | +34140506071 | 403  |
    | 10.0.3.2  | 5061 |        | +34140506071 | 403  |

  Scenario: unkown destination number
    Given the following providers exist in the address table of the database:
      | grp | ip_addr   | mask | port | tag |
      | 2   | 10.0.3.10 | 32   | 5060 | 200 |
      | 2   | 10.0.3.20 | 32   | 5060 | 201 |
    Given the following IPBXs exist in the address table of the database:
      | grp | ip_addr  | mask | port | tag |
      | 1   | 10.0.3.2 | 32   | 5060 | 100 |
      | 1   | 10.0.3.3 | 32   | 5060 | 101 |
    And the following rules exist in the dialplan table of database:
      | dpid | pr | match_op | match_exp          | match_len | subst_exp | repl_exp | attrs |
      | 2    | 1  | 1        | ^\\+33[1-9][0-9]+$ | 12        | 1         | 1        | 201   |
      | 2    | 1  | 1        | ^0[1-9][0-9]+$     | 10        | 1         | 1        | 200   |
    And the following destinations exist in the dispatcher table of database:
      | setid | destination    | flags | priority | attrs            | description |
      | 200   | 10.0.3.10:5060 | 0     | 0        | sockname=public  | prov1       |
      | 201   | 10.0.3.20.5060 | 0     | 0        | sockname=public  | prov2       |
    When SBC receives an SIP INVITE from this source "<ip>"/"<port>" with one of this "<number>" in R-URI userpart
    Then SBC generates a response to provider with this "<code>"

  Examples:
    | ip        | port | number       | code |
    | 10.0.3.2  | 5060 | 33240506070  | 404  |
    | 10.0.3.2  | 5060 | +34140506071 | 404  |
    | 10.0.3.3  | 5060 | 1240506070   | 404  |

  Scenario: known destination number but unkown destination
    Given the following providers exist in the address table of the database:
      | grp | ip_addr   | mask | port | tag |
      | 2   | 10.0.3.10 | 32   | 5060 | 200 |
      | 2   | 10.0.3.20 | 32   | 5060 | 201 |
    Given the following IPBXs exist in the address table of the database:
      | grp | ip_addr  | mask | port | tag |
      | 1   | 10.0.3.2 | 32   | 5060 | 100 |
      | 1   | 10.0.3.3 | 32   | 5060 | 101 |
    And the following rules exist in the dialplan table of database:
      | dpid | pr | match_op | match_exp          | match_len | subst_exp | repl_exp | attrs |
      | 2    | 1  | 1        | ^\\+33[1-9][0-9]+$ | 12        | 1         | 1        | 203   |
      | 2    | 1  | 1        | ^0[1-9][0-9]+$     | 10        | 1         | 1        | 203   |
    And the following destinations exist in the dispatcher table of database:
      | setid | destination    | flags | priority | attrs            | description |
      | 200   | 10.0.3.10:5060 | 0     | 0        | sockname=public  | prov1       |
      | 201   | 10.0.3.20.5060 | 0     | 0        | sockname=public  | prov2       |
    When SBC receives an SIP INVITE from this source "<ip>"/"<port>" with one of this "<number>" in R-URI userpart
    Then SBC generates a response to provider with this "<code>"

  Examples:
    | ip        | port | number       | code |
    | 10.0.3.2  | 5060 | 33240506070  | 404  |
    | 10.0.3.2  | 5060 | +33140506071 | 404  |
    | 10.0.3.3  | 5060 | 0240506070   | 404  |