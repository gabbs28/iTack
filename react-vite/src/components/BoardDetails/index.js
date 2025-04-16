import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useParams } from 'react-router-dom';

import { getBoardDetails, removeOnePinFromBoard } from '../../store/boards';
import { getAllPins } from '../../store/pins';

import Card from '../PictureCard';
import EditBoardModal from '../EditBoard/EditBoardModal';
import './index.css';

export const BoardDetails = () => {
    const dispatch = useDispatch();
    const { boardId } = useParams();

    const currentBoard = useSelector(state => state.boards);
    const user = useSelector(state => state.session?.user);

    useEffect(() => {
        dispatch(getBoardDetails(boardId));
        dispatch(getAllPins());
    }, [dispatch, boardId]);

    const handleRemovePinFromBoard = async (e) => {
        const payload = {
            boardId,
            pinId: e.target.value,
        };
        dispatch(removeOnePinFromBoard(payload));
    };

    if (!currentBoard || !currentBoard.pins) {
        return <div>Loading board...</div>;
    }

    return (
        <div className="boards-details-page-container">
            <div className="board-info-container">
                <h2 className="board-title-details">{currentBoard.title}</h2>
                <button className="user-info-button">
                    {user?.first_name?.[0]}
                </button>
                <p className="number-of-pins">{currentBoard.pins.length} Pins</p>
                <EditBoardModal />
            </div>

            <div className="unorganized-pins-container">
                {currentBoard.pins.map(pin => (
                    <div key={pin.id} className="image-user-container">
                        <button
                            value={pin.id}
                            onClick={handleRemovePinFromBoard}
                            className="delete-pin-from-board"
                        >
                            Delete from Board
                        </button>

                        <Link to={`/pins/${pin.id}`} className="user-pins-container">
                            <Card
                                src={pin?.media_url}
                                alt={pin?.description}
                            />
                        </Link>

                        <Link to="#" className="pin-owner">
                            <div>{pin?.profileUser?.username}</div>
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
};
