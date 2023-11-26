// Component accept text, placeholder values and also pass what type of Input - input, textarea so that we can use it for styling accordingly
import React, { useState, KeyboardEvent } from "react";

interface EditableProps {
    text: string;
    type: string;
    placeholder: string;
    children: React.ReactNode;
}
/*
- It will display a label is `isEditing` is false
- It will display the children (input or textarea) if `isEditing` is true
- when input `onBlur`, we will set the default non edit mode
Note: For simplicity purpose, I removed all the classnames, you can check the repo for CSS styles
*/

const Editable: React.FC<EditableProps> = ({
    text,
    type,
    placeholder,
    children,
    ...props
}) => {
    const [isEditing, setEditing] = useState(false);

    const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>, type: string) => {
        // Handle when key is pressed
    };

    return (
        <section {...props}>
            {isEditing ? (
                <div onBlur={() => setEditing(false)} onKeyDown={(e) => handleKeyDown(e, type)}>
                    {children}
                </div>
            ) : (
                <div onClick={() => setEditing(true)}>
                    <span>{text || placeholder || "Editable content"}</span>
                </div>
            )}
        </section>
    );
};

export default Editable;

