# main.py
import streamlit as st
from datetime import datetime
from conexion import db
from login import login


def main():
    login()

if __name__ == "__main__":
    main()