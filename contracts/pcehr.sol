pragma solidity ^0.4.0;


contract PCEHR {

    struct Patient {
        bytes32 proxyId;
        bytes32 pubKey;
    }

    struct RecordsSet {
        bool exists;
        bytes32 proxyId;
    }

    struct RecordsRecepient {
        bytes32 realWorldId;
        bytes32 proxyId;
        bytes32 pubKey;
    }

    struct RecepientRights {
        bool canRead;
        bool canExtend;
    }

    mapping (address => Patient) public patients;
    mapping (address => RecordsRecepient) public recepients;
    mapping (address => mapping (string => RecordsSet)) recordsSets;
    mapping (address => mapping (address => mapping (string => RecepientRights))) recepientsRights;

    modifier onlyRegisteredPatient() {
        require(
            patients[msg.sender].proxyId != bytes32(0x0), 
            "Sender is not registered"
        );
        _;
    }

    modifier onlyHasReadRightsRecepient(address _patientAddress, string _recordsType) {
        require(
            recepientsRights[_patientAddress][msg.sender][_recordsType].canRead,
            "Sender has no read rights for this records set"
        );
        _;
    }

    modifier onlyHasExtendRightsRecepient(address _patientAddress, string _recordsType) {
        require(
            recepientsRights[_patientAddress][msg.sender][_recordsType].canExtend,
            "Sender has no write rights for this records set"
        );
        _;
    }

    modifier onlyRecordsSetOwner(string _recordsType) {
        require(
            recordsSets[msg.sender][_recordsType].exists,
            "Sender is not owner of this records set"
        );
        _;
    }

    modifier onlyNonExistedRecordsSet(string _recordsType) {
        require(
            !recordsSets[msg.sender][_recordsType].exists,
            "Records set with this proxyId already exists"
        );
        _;
    }

    event PatientInChain(
        address _address,
        bytes32 _pubKey,
        bytes32 indexed _patientProxyId
    );

    event RecepientInChain(
        address _address,
        bytes32 _pubKey,
        bytes32 indexed _recepientProxyId,
        bytes32 indexed _realWorldId
    );

    event RecordsSetAdded(
        address _addedBy,
        bytes32 _recordsSetProxyId,
        string _recordsType
    );

    event RecordsSetExtended(
        address _extendedBy,
        bytes32 _recordsSetProxyId
    );

    event AllowedExtendAccessToRecordsSet(
        bytes32 _recordsSetProxyId,
        address indexed _recepientAddress
    );

    event AllowedReadAccessToRecordsSet(
        bytes32 _recordsSetProxyId,
        address indexed _toRecepientAddress
    );


    function registerPatient(
        bytes32 _patientProxyId,
        bytes32 _patientPubKey
    ) public {
        var patient = Patient(_patientProxyId, _patientPubKey);
        patients[msg.sender] = patient;

        emit PatientInChain(
            msg.sender,
            _patientPubKey,
            _patientProxyId
        );

    }

    function registerRecepient(
        bytes32 _recepientProxyId,
        bytes32 _recepientPubKey,
        bytes32 _recepientRealWorldId
    ) public {
        var recepient = RecordsRecepient(
            _recepientProxyId,
            _recepientPubKey,
            _recepientRealWorldId
        );
        recepients[msg.sender] = recepient;

        emit RecepientInChain(
            msg.sender,
            _recepientPubKey,
            _recepientProxyId,
            _recepientRealWorldId
        );
    }

    function addRecordsSet(
        address _patientAddress,
        bytes32 _proxyId,
        string _recordsType
    ) 
    public
    onlyHasExtendRightsRecepient(_patientAddress, _recordsType)
    {
        recordsSets[_patientAddress][_recordsType] = RecordsSet(true, _proxyId);
        emit RecordsSetAdded(msg.sender, _proxyId, _recordsType);       
    }

    function extendRecordsSet(
        bytes32 _recordsSetId,
        bytes32 _recordsRecepientId
    ) public {}

    function allowRecordsSetReadRights(
        bytes32 _recordsSetId,
        address _toRecepientAddress
    ) public {}

    function allowRecordsSetExtendRights(
        bytes32 _dataSetId,
        bytes32 _toRecepientProxyId
    ) public {}
}
