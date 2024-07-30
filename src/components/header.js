import React, { useState } from 'react';

function Header() {
  const [isDropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setDropdownOpen(!isDropdownOpen);
  };

  return (
    <header>
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li>
            <button onClick={toggleDropdown}>
              Services
            </button>
            {isDropdownOpen && (
              <ul className="dropdown">
                <li><a href="/service1">Service 1</a></li>
                <li><a href="/service2">Service 2</a></li>
                <li><a href="/service3">Service 3</a></li>
              </ul>
            )}
          </li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
