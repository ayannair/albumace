import React, {useState, useEffect} from "react";

const SearchBar=  ({onSearch}) => {
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        onSearch(searchTerm);
    }, [searchTerm, onSearch]);

    const handleInputChange = (event) => {
        setSearchTerm(event.target.value);
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '20px' }}>
          <input
            type="text"
            placeholder="Search..."
            value={searchTerm}
            onChange={handleInputChange}
          />
        </div>
    );
};
    
    export default SearchBar;