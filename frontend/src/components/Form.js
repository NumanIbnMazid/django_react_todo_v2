import React, { Component } from "react";
import {
    Button,
    Form,
    FormGroup,
    Input,
} from "reactstrap";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { notify } from "../helpers/Helper"


export default class CustomModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeItem: this.props.activeItem,
            todoList: this.props.todoList,
        };
    }

    handleReset = () => {
        Array.from(document.querySelectorAll("input")).forEach(
            input => (input.value = "")
        );
        // clear input and active state
        this.setState({
            activeItem: { title: '', description: '', priority: 1, is_completed: false, flag: 0, is_updated: false }
        });
    };

    handleSubmit = (saveMethod) => {
        if (this.state.activeItem.title.length > 0) {
            saveMethod(this.state.activeItem)
            // clear form  and active state
            this.handleReset()
        } else {
            notify("Please enter a task name", "error");
        }
    }

    handleChange = (e) => {
        let { name, value } = e.target;

        if (e.target.type === "checkbox") {
            value = e.target.checked;
        }

        const activeItem = { ...this.state.activeItem, [name]: value };

        this.setState({ activeItem });
    };

    render() {
        const { onSave } = this.props;
        return (
            <Form id="task-form">
                <FormGroup>
                    <div className="row">
                        <div className="col-lg-10 col-md-10 col-sm-10 col-6">
                            <Input
                                type="text"
                                id="todo-title"
                                name="title"
                                value={this.state.activeItem.title}
                                onChange={this.handleChange}
                                placeholder="Task name"
                                className="p-3"
                                required={true}
                            />
                        </div>
                        <div className="col-lg-2 col-md-2 col-sm-2 col-6">
                            <div>
                                <Button
                                    className="bg-bluish border-0 rounded"
                                    onClick={() => this.handleSubmit(onSave)}
                                >
                                    <FontAwesomeIcon icon="plus" className="display-6 text-primary" />
                                </Button>
                            </div>
                        </div>
                    </div>

                </FormGroup>
            </Form>
        );
    }
}