Feature: marginCalcul
    In order to get our final price


    Scenario Outline: marginCalcul
        Given I have a <minPrice>
        When I add <margin>
        Then I should got <price>

        Examples:
        | minPrice | margin | price |
        |    12    |    5   |   7   |
        |    20    |    5   |   15  |
