from flask import Flask, render_template, url_for, request, redirect, abort
from misc import *

'''Check models and maps exist'''
check_and_move_models_knn()
check_and_move_models_linear()
check_and_move_maps()