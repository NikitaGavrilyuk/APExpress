import React, { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';

function SearchBox() {
  const navigate = useNavigate();
  const location = useLocation();
  const [history, setHistory] = useState([]);
  const [keyword, setKeyword] = useState('');

  const submitHandler = (e) => {
    e.preventDefault();
    if (keyword) {
      setHistory([...history, `/?keyword=${keyword}`]);
      navigate(`/?keyword=${keyword}&page=1`);
    } else {
      if (history.length > 0) {
        setHistory([...history, history[history.length - 1]]);
      }
    }
  };

  return (
    <Form onSubmit={submitHandler} className="d-flex">
      <Form.Control
        type="text"
        name="q"
        onChange={(e) => setKeyword(e.target.value)}
        className="mr-2"
        placeholder="Search"
      ></Form.Control>
      <Button type="submit" variant="dark" className="p-2">
        Submit
      </Button>
    </Form>
  );
}

export default SearchBox;
