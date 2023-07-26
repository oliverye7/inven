#!/bin/bash

# Define the inven function as an alias to ./inven
inven() {
  ./inven "$@"
}

# Export the inven function
export -f inven
