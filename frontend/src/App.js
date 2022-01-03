import React, { Component } from "react";
import Form from "./components/Form";
import DeleteModal from "./components/DeleteModal";
import ClearModal from "./components/ClearModal";
import axios from "./axios";

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import {
  Button,
  Input,
} from "reactstrap";

import { handleApiResponseExceptionMessage, notify } from "./helpers/Helper"

import fontawesome from '@fortawesome/fontawesome';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus, faPlusCircle, faList, faTimes } from '@fortawesome/free-solid-svg-icons';


fontawesome.library.add(faPlus, faPlusCircle, faList, faTimes);

class App extends Component {
  constructor(props) {
    super(props);

    // toastr config
    this.contextClass = {
      success: "bg-success",
      error: "bg-danger",
      info: "bg-info",
      warning: "bg-warning",
      default: "bg-primary",
      dark: "bg-dark text-white",
    };
    this.state = {
      viewCompleted: false,
      viewAll: false,
      todoList: [],
      deleteModal: false,
      clearModal: false,
      activeItem: {
        title: "",
        description: "",
        is_completed: false,
        priority: 1,
        is_updated: false,
        flag: 0, // 0: unsynced, 1: synced
      },
    };
  }

  componentDidMount() {
    this.refreshList();
  }

  // List
  refreshList = () => {
    axios
      .get("todos/list/")
      .then((res) => this.setState({ todoList: res.data.data }))
      .catch((error) => handleApiResponseExceptionMessage(error));
  };

  toggleDelete = () => {
    this.setState(
      { deleteModal: !this.state.deleteModal }
    );
  };
  toggleClear = () => {
    this.setState(
      { clearModal: !this.state.clearModal }
    );
  };

  setInitialObjectState = (index) => {
    // 1. Make a shallow copy of the items
    let todoList = [...this.state.todoList];
    // 2. Make a shallow copy of the item to mutate
    let todo = { ...todoList[index] };
    // 3. Replace the property
    todo.is_updated = false
    todo.flag = 1
    // 4. Put it back into array. N.B. mutating the array here, but that's a copy made first
    todoList[index] = todo;
    // 5. Set the state to new copy
    this.setState({ ...this.state, todoList });
  }

  setIsCompletedObjectState = (index) => {
    let todoList = [...this.state.todoList];
    let todo = { ...todoList[index] };
    todo.is_completed = !todo.is_completed
    todo.is_updated = true
    todoList[index] = todo;
    this.setState({ ...this.state, todoList });
  }

  // Create & Update
  handleSubmit = (item) => {
    // check if item exists
    const found = this.state.todoList.some(el => el.title === item.title);
    if (found) {
      notify("Task already exists", "error");
      return;
    } else {
      this.state.todoList.push(item);
      this.setState({ todoList: this.state.todoList })
    }
  };

  // Create & Update
  handleSave = () => {
    let createObjects = []
    let updateObjects = []

    // loop through todoList
    this.state.todoList.forEach(item => {
      if (item.slug && item.is_updated) {
        updateObjects.push(item)
      }
      else {
        if (item.flag === 0) {
          createObjects.push(item)
        }

      }
    })

    try {
      if (createObjects.length > 0) {
        axios.post("todos/create-or-update/multiple/", createObjects)
          .then(res => {
            this.refreshList()
          })
          .catch(error => handleApiResponseExceptionMessage(error));
      }
      if (updateObjects.length > 0) {
        axios.post("todos/create-or-update/multiple/", updateObjects)
          .then(res => {
            this.refreshList()
          })
          .catch(error => handleApiResponseExceptionMessage(error));
      }
    } catch (error) {
      notify("Synchronization error!", "error");
      return
    }

    // notify
    notify("Tasks has been synchronized!", "success");
    return
  };

  // clear
  handleClear = () => {
    // toogle modal
    this.toggleClear();

    let deleteObjects = []
    let unsyncedCompletedItems = []

    // loop through todoList
    this.state.todoList.forEach(item => {
      if (item.is_completed === true && item.slug) {
        deleteObjects.push(item)
      }
      else if (item.is_completed === true && !item.slug) {
        unsyncedCompletedItems = this.state.todoList.filter(
          (item) => item.is_completed === false
        );
      }
    })

    try {
      if (deleteObjects.length > 0) {
        axios.post("todos/delete-multiple/", deleteObjects)
          .then(res => {
            // notify
            notify("All completed tasks has been removed!", "success");
            this.refreshList()
            return
          })
          .catch(error => handleApiResponseExceptionMessage(error));
      }
      else if (unsyncedCompletedItems.length > 0) {
        this.setState({ todoList: unsyncedCompletedItems })
      }
      else {
        notify("Nothing to clear!", "warning");
      }
    } catch (error) {
      notify("Synchronization error!", "error");
    }
  }

  handleIsCompletedState = (item) => {
    // find object index
    const objIndex = this.state.todoList.findIndex(obj => obj.title === item.title);
    this.setIsCompletedObjectState(objIndex)
  }

  // Patch
  handleIsCompletedPatch = (item) => {
    item.is_completed = !item.is_completed;
    const data = {
      "is_completed": item.is_completed,
    }
    if (item.slug) {
      axios
        .patch(`todos/partial/update/${item.slug}/`, data)
        .then((res) => {
          this.refreshList()
          notify("Updated Successfully!", "success")
        })
        .catch((error) => handleApiResponseExceptionMessage(error));
      return;
    }
  };

  // Delete
  handleDelete = (item) => {
    this.toggleDelete();
    if (item.slug) {
      axios
        .delete(`todos/delete/${item.slug}/`)
        .then((res) => {
          this.refreshList()
          notify("Deleted Successfully!", "success")
        })
        .catch((error) => handleApiResponseExceptionMessage(error));
    } else {
      this.state.todoList.splice(this.state.todoList.indexOf(item), 1);
      this.setState({ todoList: this.state.todoList })
    }
  };

  deleteItem = (item) => {
    this.setState({ activeItem: item, deleteModal: !this.state.deleteModal });
  };

  clearItem = (item) => {
    this.setState({ clearModal: !this.state.clearModal });
  };

  renderItems = () => {
    // render all items
    const newItems = this.state.todoList;

    if (newItems.length === 0) {
      return (
        <div className="alert alert-warning text-center fw-bold m-4" role="alert">
          No data!
        </div>
      );
    }

    else {

      return newItems.map((item, index) => (
        <div
          key={item.id || index}
          className="row p-4"
        >
          <div className="col-lg-1 col-md-1 col-sm-2 col-4">
            {/* Is Completed Checkbox */}
            <span>
              <div className="form-check">
                <Input
                  name="is_completed" className="form-check-input p-4" type="checkbox" value="" id="flexCheckChecked"
                  checked={item.is_completed}
                  onChange={() => this.handleIsCompletedState(item)}
                />
                <label className="form-check-label">
                </label>
              </div>
            </span>
          </div>
          <div className="col-lg-9 col-md-9 col-sm-8 col-4 d-flex align-items-center bg-light rounded">
            <div
              className={`text-start ${!item.is_completed ? "fw-bolder" : ""}`}
            >
              {item.title}
            </div>
          </div>
          <div className="col-lg-1 col-md-1 col-sm-2 col-4">
            <div className="text-start">
              <button
                className="btn btn-default rounded border border-2"
                onClick={() => this.deleteItem(item)}
              >
                <FontAwesomeIcon icon="times" className="display-6 text-secondary" />
              </button>
            </div>
          </div>
        </div>
      ));
    }
  };

  render() {
    return (
      <main className="">
        <nav className="navbar sticky-top navbar-light bg-primary">
          <div className="container-fluid text-center justify-content-center p-3">
            <span className="navbar-brand text-white fw-bolder">To-Do App</span>
          </div>
        </nav>

        {/* Toastr Message */}
        <ToastContainer
          style={{ width: "400px" }}
        />

        <div className="container-fluid todo-app-root rounded">

          {/* main content */}
          <div className="container mt-5">
            <div className="row">
              <div className="mx-auto">
                <div className="todo-app-content p-3">
                  <div className="m-4">
                    {/* Task Form */}
                    <Form
                      todoList={this.state.todoList}
                      activeItem={this.state.activeItem}
                      onSave={this.handleSubmit}
                    />
                  </div>

                  {/* Task List */}
                  <div className="">
                    {this.renderItems()}
                  </div>

                  {/* Task Action Button */}
                  <div className="p-4">
                    <Button className="bg-bluish border-0 rounded px-4 py-2 text-dark rounded"
                      onClick={() => this.handleSave()}
                    >
                      <span className="fs-5 fw-bold">Save</span>
                    </Button>
                    <Button className="bg-bluish border-0 rounded px-4 py-2 text-dark rounded ms-4"
                      onClick={() => this.clearItem()}
                    >
                      <span className="fs-5 fw-bold">Clear</span>
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {this.state.deleteModal ? (
            <DeleteModal
              activeItem={this.state.activeItem}
              toggle={this.toggleDelete}
              onDelete={this.handleDelete}
            />
          ) : null}
          {this.state.clearModal ? (
            <ClearModal
              toggle={this.toggleClear}
              onClear={this.handleClear}
            />
          ) : null}

        </div>
      </main>
    );
  }
}

export default App;