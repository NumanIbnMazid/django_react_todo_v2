import React, { Component } from "react";
import {
    Button,
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
} from "reactstrap";

export default class CustomModal extends Component {
    render() {
        const { toggle, onClear } = this.props;

        return (
            <Modal isOpen={true} toggle={toggle}>
                <ModalHeader toggle={toggle}>Please Confirm</ModalHeader>
                <ModalBody>
                    <div className="text-center">
                        <h5 className="fw-bold">Are you sure you want to delete all completed tasks?</h5>
                    </div>
                </ModalBody>
                <ModalFooter>
                    <Button color="secondary" onClick={toggle}>
                        Cancel
                    </Button>
                    <Button
                        color="danger"
                        onClick={() => onClear()}
                    >
                        Delete
                    </Button>
                </ModalFooter>
            </Modal>
        );
    }
}