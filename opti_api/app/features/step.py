from lettuce import *

@step('I have a (\d+)')
def have(step, price):
    world.price = world.price

@step('I add (\d+)')
def add(step, number):
    world.number = world.number * 2

@step('I should got (\d+)')
def shouldGot(step, expected):
    assert expected * 2 == world.number
